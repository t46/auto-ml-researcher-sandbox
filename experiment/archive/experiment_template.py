from prompt2model.dataset_retriever import DescriptionDatasetRetriever
from prompt2model.prompt_parser import MockPromptSpec, TaskType
from prompt2model.prompt_parser import PromptBasedInstructionParser, TaskType

from prompt2model.utils import api_tools


# CHANGE THIS if you want to try a different model
api_tools.default_api_agent = api_tools.APIAgent(model_name="gpt-3.5-turbo", max_tokens=1000)

# データセットの取得  TODO: ここ全部丸ごと抽象化しても良い
retriever = DescriptionDatasetRetriever()

task_type = TaskType.TEXT_GENERATION
prompt_text = """
sentiment analysis
"""
prompt_spec = PromptBasedInstructionParser(task_type=TaskType.TEXT_GENERATION)
prompt_spec._instruction = prompt_text

sorted_list = retriever.retrieve_top_datasets(prompt_spec)
top_dataset_info = retriever.rerank_datasets(sorted_list, prompt_spec)  # TODO: rerank は最も合致するものしか取ってこないので、rerank -> sorted_list から除外　-> 再 rerank として2番目以降も取得する
dataset_dict = retriever.canonicalize_dataset_automatically(
    top_dataset_info, prompt_spec, auto_transform_data=True, num_points_to_transform=5
)

# dataset_dict = retriever.retrieve_dataset_dict(prompt_spec, auto_transform_data=True, num_points_to_transform=1)

print(dataset_dict)

# from transformers import AutoModel, AutoTokenizer, pipeline
# from datasets import load_dataset
# from prompt2model.dataset_retriever import DescriptionDatasetRetriever

# # Example usage
# model_name = "distilbert-base-uncased-finetuned-sst-2-english"
# dataset_name = "squad"

# # Load the model and tokenizer
# model = AutoModel.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# # Load the dataset
# dataset = load_dataset(dataset_name)

# # Create a pipeline for inference
# nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

# # Run inference on the dataset
# results = nlp(dataset["text"])

# # Print the results
# for result in results:
#     print(f"Text: {result['text']}")
#     print(f"Label: {result['label']}")
#     print(f"Score: {result['score']}")
#     print("---")