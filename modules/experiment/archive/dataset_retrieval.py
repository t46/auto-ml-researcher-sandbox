"""A dual-encoder dataset retriever using HuggingFace dataset descriptions."""

import json
import os
import random
import urllib.request
import numpy as np

import datasets
import torch
from transformers import AutoTokenizer, AutoModel

class DatasetInfo:
    def __init__(self, name, description, score):
        self.name = name
        self.description = description
        self.score = score

class DescriptionDatasetRetriever:
    def __init__(self, search_index_path="huggingface_data/huggingface_datasets/huggingface_datasets_datafinder_index",
                 first_stage_search_depth=1000, max_search_depth=25, 
                 encoder_model_name="sentence-transformers/all-mpnet-base-v2", device=None,
                 max_number_of_dataset_rows=3000, allow_gated_datasets=False):
        self.search_index_path = search_index_path
        self.first_stage_search_depth = first_stage_search_depth
        self.max_search_depth = max_search_depth
        self.encoder_model_name = encoder_model_name
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_number_of_dataset_rows = max_number_of_dataset_rows
        self.allow_gated_datasets = allow_gated_datasets
        self.tokenizer = AutoTokenizer.from_pretrained(encoder_model_name)
        self.model = AutoModel.from_pretrained(encoder_model_name).to(self.device)
        self.initialize_search_index()

    def initialize_search_index(self):
        self.dataset_infos = []
        os.makedirs(os.path.dirname(self.search_index_path), exist_ok=True)
        self.full_dataset_metadata = self.download_json_file(self.search_index_path, 
            "http://phontron.com/data/prompt2model/dataset_index.json")
        for name in sorted(self.full_dataset_metadata):
            self.dataset_infos.append(DatasetInfo(name, self.full_dataset_metadata[name]["description"], 0.0))
        
        self.reranking_datasets_infos = self.download_json_file(self.search_index_path.replace("_index", "_reranking_index"), 
            "http://phontron.com/data/prompt2model/dataset_reranking_index.json")

        if not os.path.exists(self.search_index_path):
            self.encode_text([x.description for x in self.dataset_infos], self.search_index_path)
            
    def download_json_file(self, path, url):
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
        return json.load(open(path))
    
    def encode_text(self, texts, output_file):
        embeddings = []
        with torch.no_grad():
            for text in texts:
                inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
                embedding = self.model(**inputs).pooler_output.cpu().numpy()
                embeddings.append(embedding)
        embeddings = torch.from_numpy(np.concatenate(embeddings, axis=0))
        torch.save(embeddings, output_file)
        return embeddings

    def retrieve_objects(self, query_vector, search_index_file, object_names, top_k):
        index_vectors = torch.load(search_index_file).float()
        query_vector = torch.from_numpy(query_vector).float()
        scores = torch.mv(index_vectors, query_vector)
        top_indices = torch.topk(scores, top_k).indices
        return [(object_names[i], scores[i].item()) for i in top_indices]
    
    def canonicalize_dataset_using_columns(self, dataset, input_columns, output_column):
        dataset_dict = {}
        for split in dataset:
            input_col = []
            output_col = []
            for i in range(min(len(dataset[split]), self.max_number_of_dataset_rows)):
                curr_string = "\n".join(f"{col}: {dataset[split][i][col]}" for col in input_columns)
                input_col.append(curr_string)
                output_col.append(dataset[split][i][output_column])
            dataset_dict[split] = datasets.Dataset.from_dict({"input_col": input_col, "output_col": output_col})
        return datasets.DatasetDict(dataset_dict)

    def get_dataset_infos(self, dataset_list):
        dataset_info_dict = {}
        for dataset_name in dataset_list:
            if dataset_name not in self.reranking_datasets_infos or \
                self.reranking_datasets_infos[dataset_name]["is_gated"] != self.allow_gated_datasets:
                continue
            dataset = self.reranking_datasets_infos[dataset_name]
            if len(dataset["configs"]) > 5:
                dataset["configs"] = dict(random.sample(list(dataset["configs"].items()), 5))
            dataset_info_dict[dataset_name] = dataset
        return dataset_info_dict

    def automatic_column_selection(self, instruction, dataset_name, description, columns, example_rows):
        prompt = self.construct_prompt_for_column_selection(instruction, dataset_name, description, columns, example_rows)
        response = self.parse_prompt(prompt, ["input", "output"], ["ambiguous", "irrelevant"])
        input_columns, output_column = response["input"], response["output"]
        if len(input_columns) < 1 or len(output_column) != 1 or \
            any(col not in columns for col in input_columns + output_column):
            raise ValueError("Invalid columns selected")
        return input_columns, output_column[0]

    def construct_prompt_for_column_selection(self, instruction, dataset_name, description, columns, example_rows):
        prompt = f"Instruction: {instruction}\n\nDataset: {dataset_name}\nDescription: {description}\nColumns: {', '.join(columns)}\n\nExample Rows:\n"
        for i, row in enumerate(example_rows):
            prompt += f"Row {i+1}:\n"
            for col, val in row.items():
                prompt += f"{col}: {val}\n"
            prompt += "\n"
        prompt += "Given the instruction and the dataset information, which columns should be used as input and output? Provide the input columns separated by commas and the output column."
        return prompt

    def parse_prompt(self, prompt, required_keys, optional_keys):
        # Placeholder for parsing the prompt response
        # Replace with actual parsing logic
        return {"input": ["col1", "col2"], "output": ["col3"]}

    def retrieve_top_datasets(self, instruction):
        query_vector = self.encode_text([instruction], "query_vector.pt")[0]
        ranked_list = self.retrieve_objects(query_vector, self.search_index_path, 
                                            [x.name for x in self.dataset_infos], self.first_stage_search_depth)
        dataset_name_to_dataset_idx = {d.name: i for i, d in enumerate(self.dataset_infos)}
        for dataset_name, dataset_score in ranked_list:
            self.dataset_infos[dataset_name_to_dataset_idx[dataset_name]].score = dataset_score
        return [x.name for x in sorted(self.dataset_infos, key=lambda x: x.score, reverse=True)[:self.max_search_depth]]

    def rerank_datasets(self, dataset_list, instruction):
        dataset_info_dict = self.get_dataset_infos(dataset_list)
        if not dataset_info_dict:
            return None
        prompt = self.construct_prompt_for_dataset_reranking(instruction, dataset_info_dict)
        response = self.parse_prompt(prompt, module_name="rerank")
        dataset_name, config_name, confidence_level = response["dataset_name"], response["config_name"], response["confidence_level"]
        if dataset_name not in dataset_info_dict or config_name not in dataset_info_dict[dataset_name]["configs"] or confidence_level == "low":
            return None
        return dataset_info_dict[dataset_name]["configs"][config_name]

    def construct_prompt_for_dataset_reranking(self, instruction, dataset_info_dict):
        prompt = f"Instruction: {instruction}\n\nDatasets:\n"
        for dataset_name, dataset_info in dataset_info_dict.items():
            prompt += f"Dataset: {dataset_name}\nDescription: {dataset_info['dataset_description']}\nColumns: {', '.join(dataset_info['columns'])}\n\n"
        prompt += "Which dataset is most suitable for the given instruction? Provide the dataset name, config name, and your confidence level (high, medium, low)."
        return prompt

    def retrieve_dataset_dict(self, instruction):
        sorted_list = self.retrieve_top_datasets(instruction)
        top_dataset_info = self.rerank_datasets(sorted_list, instruction)
        if not top_dataset_info:
            return None
        
        full_dataset = datasets.load_dataset(top_dataset_info["dataset_name"], top_dataset_info["config_name"]).shuffle().flatten()
        full_dataset = full_dataset.rename_columns(top_dataset_info["columns_mapping"])
        
        try:
            input_columns, output_column = self.automatic_column_selection(instruction, top_dataset_info["dataset_name"], 
                                                                           top_dataset_info["dataset_description"],
                                                                           top_dataset_info["columns"], 
                                                                           top_dataset_info["sample_row"])
        except ValueError:
            return None
        
        return self.canonicalize_dataset_using_columns(full_dataset, input_columns, output_column)
    

if __name__ == '__main__':
    instruction = """
    classify news articles
    """

    retriever = DescriptionDatasetRetriever()
    dataset = retriever.retrieve_dataset_dict(instruction=instruction)

    print(dataset)