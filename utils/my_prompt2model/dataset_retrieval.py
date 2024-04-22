"""An dual-encoder dataset retriever using HuggingFace dataset descriptions."""

from __future__ import annotations  # noqa FI58

import json
import os
import urllib.request

import datasets
import torch
import dataclasses
import logging
from utils.my_prompt2model.encode import encode_text
from utils.my_prompt2model.retrieve import retrieve_objects

@dataclasses.dataclass
class DatasetInfo:
    """Store the dataset name, description, and query-dataset score for each dataset.

    Args:
        name: The name of the dataset.
        description: The description of the dataset.
        score: The retrieval score of the dataset.
    """

    name: str
    description: str
    score: float


def get_formatted_logger(logger_name: str):
    """Create a formatted logger.

    Args:
        logger_name: The name of the logger, usually the name
            of the component that uses the logger.

    Returns:
        A logger object.
    """
    logger = logging.getLogger(logger_name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

datasets.utils.logging.disable_progress_bar()
logger = get_formatted_logger("DescriptionDatasetRetriever")


class DescriptionDatasetRetriever:
    """Retrieve a dataset from HuggingFace, based on similarity to the prompt."""

    def __init__(
        self,
        search_index_path: str = "huggingface_data/huggingface_datasets/"
        + "huggingface_datasets_datafinder_index",
        first_stage_search_depth: int = 1000,
        max_search_depth: int = 25,
        encoder_model_name: str = "viswavi/datafinder-huggingface-prompt-queries",
        dataset_info_file: str = "huggingface_data/huggingface_datasets/"
        + "dataset_index.json",
        reranking_dataset_info_file="huggingface_data/huggingface_datasets/"
        + "reranking_dataset_index.json",
        device: torch.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        ),
        max_number_of_dataset_rows=3000,
        allow_gated_datasets=False,
    ):
        """Initialize a dual-encoder retriever against a search index.

        Args:
            search_index_path: Where to store the search index (e.g. encoded vectors).
            first_stage_search_depth: The # of datasets to retrieve before filtering.
            max_search_depth: The number of most-relevant datasets to retrieve.
            encoder_model_name: The name of the model to use for the dual-encoder.
            dataset_info_file: The file containing dataset names and descriptions.
            reranking_dataset_info_file: File containing dataset info used for reranking
            device: The device to use for encoding text for our dual-encoder model.
            max_number_of_dataset_rows: Limit the number of rows for large datasets.
            allow_gated_datasets: Use only if the user explicitly wants gated datasets
        """
        self.search_index_path = search_index_path
        self.first_stage_search_depth = first_stage_search_depth
        self.max_search_depth = max_search_depth
        self.encoder_model_name = encoder_model_name
        self.device = device
        self.dataset_info_file = dataset_info_file
        self.reranking_dataset_info_file = reranking_dataset_info_file
        self.max_number_of_dataset_rows = max_number_of_dataset_rows
        self.allow_gated_datasets = allow_gated_datasets
        self.initialize_search_index()

    def initialize_search_index(self) -> None:
        """Initialize the search index."""
        self.dataset_infos: list[DatasetInfo] = []
        if not os.path.exists(self.dataset_info_file):
            # Download the dataset search index if one is not on disk already.
            logger.info("Downloading the dataset search index")
            os.makedirs(os.path.dirname(self.dataset_info_file), exist_ok=True)
            urllib.request.urlretrieve(
                "http://phontron.com/data/prompt2model/dataset_index.json",
                self.dataset_info_file,
            )
        self.full_dataset_metadata = json.load(open(self.dataset_info_file, "r"))
        for dataset_name in sorted(self.full_dataset_metadata.keys()):
            self.dataset_infos.append(
                DatasetInfo(
                    name=dataset_name,
                    description=self.full_dataset_metadata[dataset_name]["description"],
                    score=0.0,
                )
            )
        if not os.path.exists(self.reranking_dataset_info_file):
            # Download the reranking index if one is not on disk already.
            logger.info("Downloading the Reranking Dataset Index File")
            urllib.request.urlretrieve(
                "http://phontron.com/data/prompt2model/dataset_reranking_index.json",
                self.reranking_dataset_info_file,
            )
        with open(self.reranking_dataset_info_file, "r") as f:
            self.reranking_datasets_infos = json.load(f)

        if os.path.isdir(self.search_index_path):
            raise ValueError(
                "Search index must either be a valid file or not exist yet. "
                "But {self.search_index_path} is provided."
            )
        if not os.path.exists(self.search_index_path):
            logger.info("Creating dataset descriptions")
            encode_text(
                self.encoder_model_name,
                text_to_encode=[x.description for x in self.dataset_infos],
                encoding_file=self.search_index_path,
                device=self.device,
            )

    def retrieve_top_datasets(
        self,
        prompt: str,
    ) -> list[str]:
        """Retrieve the top datasets for a prompt.

        Specifically, the datasets are scored using a dual-encoder retriever model
        and the datasets with the highest similarity scores with the query are returned.

        Args:
            prompt_spec: A prompt.

        Returns:
            A list of the top datasets for the prompt according to retriever score.
        """
        query_vector = encode_text(
            self.encoder_model_name,
            text_to_encode=prompt,
            device=self.device,
        )

        ranked_list = retrieve_objects(
            query_vector,
            self.search_index_path,
            [x.name for x in self.dataset_infos],
            self.first_stage_search_depth,
        )
        top_dataset_infos = []
        dataset_name_to_dataset_idx = {
            d.name: i for i, d in enumerate(self.dataset_infos)
        }
        for dataset_name, dataset_score in ranked_list:
            dataset_idx = dataset_name_to_dataset_idx[dataset_name]
            self.dataset_infos[dataset_idx].score = dataset_score
            top_dataset_infos.append(self.dataset_infos[dataset_idx])

        sorted_list = sorted(top_dataset_infos, key=lambda x: x.score, reverse=True)[
            : self.max_search_depth
        ]
        if len(sorted_list) == 0:
            raise ValueError("No datasets retrieved from search index.")
        dataset_names = [x.name for x in sorted_list]
        return dataset_names