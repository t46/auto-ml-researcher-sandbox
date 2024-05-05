from prompt2model.dataset_retriever import DescriptionDatasetRetriever
from prompt2model.model_retriever import DescriptionModelRetriever
from prompt2model.prompt_parser import MockPromptSpec, TaskType
from prompt2model.prompt_parser import PromptSpec
from prompt2model.dataset_retriever.reranking_prompt import construct_prompt_for_dataset_reranking
import random
from prompt2model.utils import get_formatted_logger
import types

logger = get_formatted_logger("DescriptionDatasetRetriever")


# NOTE: データセット名を返すために、rerank_datasetsをオーバーライド
def rerank_datasets_with_name_saved(
    self, datasets_info: dict, prompt_spec: PromptSpec
) -> tuple[str | None, str | None]:
    """Rerank datasets based on relevance to a given prompt specification.

    This function takes a list of datasets and a prompt specification,
    and reranks the datasets based on their relevance to the prompt. It
    first gathers detailed information about each dataset in the list using the
    `get_all_dataset_infos` method. Then, it constructs a prompt for reranking
    and parses its response to identify the most relevant dataset and
    configuration. The function also includes checks for the validity of the
    response(hallucinations) and the confidence level of the dataset
    recommendation.

    Args:
        datasets_info: The datasets to be considered
        prompt_spec: An object containing the prompt specification,
                    ncluding instruction and examples, used for reranking datasets.

    Returns:
        dict or None: The most relevant dataset configuration, or None if
            no suitable dataset is found or if the confidence level
            in the recommendation is low.
    """
    dataset_selection_prompt = construct_prompt_for_dataset_reranking(
        prompt_spec.instruction, prompt_spec.examples, datasets_info
    )
    dataset_name = self.get_rerank_with_highest_votes(
        prompt=dataset_selection_prompt, infos_dict=datasets_info
    )

    if dataset_name is None:
        return None, None

    if len(datasets_info[dataset_name]["configs"].keys()) == 1:
        config_name = list(datasets_info[dataset_name]["configs"].keys())[0]

    else:
        curr_dataset = datasets_info[dataset_name]
        if len(curr_dataset["configs"]) > 10:
            curr_dataset["configs"] = dict(
                random.sample(list(curr_dataset["configs"].items()), 10)
            )
        config_selection_prompt = construct_prompt_for_dataset_reranking(
            prompt_spec.instruction,
            prompt_spec.examples,
            curr_dataset,
            is_config=True,
        )
        config_name = self.get_rerank_with_highest_votes(
            config_selection_prompt, curr_dataset["configs"]
        )

    logger.info(f"Chosen dataset and config: {dataset_name=} {config_name=}")
    # config name being None gets handled in calling function

    self.top_dataset_name = dataset_name  # NOTE: Save the top dataset name

    return dataset_name, config_name

def retrieve_dataset(prompt_text, task_type):
    task_type = TaskType.TEXT_GENERATION
    prompt_spec = MockPromptSpec(task_type)
    prompt_spec._instruction = prompt_text
    retriever = DescriptionDatasetRetriever()
    retriever.rerank_datasets = types.MethodType(rerank_datasets_with_name_saved, retriever)  # 
    dataset_dict = retriever.retrieve_dataset_dict(prompt_spec)
    dataset_name = retriever.top_dataset_name
    return dataset_name, dataset_dict

def retrieve_model(prompt_text, task_type):
    task_type = TaskType.TEXT_GENERATION
    prompt_spec = MockPromptSpec(task_type)
    prompt_spec._instruction = prompt_text
    retriever = DescriptionModelRetriever(
        search_depth=5,
        use_bm25=True,
        use_HyDE=True
    )
    top_model_names = retriever.retrieve(prompt_spec)
    return top_model_names


if __name__ == '__main__':
    prompt_text = "Make toxic comments less toxic."
    task_type = TaskType.TEXT_GENERATION
    dataset_name, dataset_dict = retrieve_dataset(prompt_text, task_type)
    model_names = retrieve_model(prompt_text, task_type)
    print(dataset_name)
    print(dataset_dict)
    print(model_names)