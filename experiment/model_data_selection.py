from prompt2model.dataset_retriever import DescriptionDatasetRetriever
from prompt2model.prompt_parser import TaskType
from prompt2model.prompt_parser import PromptBasedInstructionParser, TaskType
from prompt2model.model_retriever import DescriptionModelRetriever
from prompt2model.utils import api_tools


# CHANGE THIS if you want to try a different model
api_tools.default_api_agent = api_tools.APIAgent(model_name="gpt-3.5-turbo", max_tokens=1000)  # TODO: max_tokens のところは無理やりやってるだけなので後で直す

def select_data(problem: str, proposed_method: str, experiment_design: str) -> str:

    # データセットの取得  TODO: ここ全部丸ごと抽象化しても良い
    prompt_text = f"""
    Task: You will verify the effectiveness of the proposed method that is expected to solve the following problem using the experimental plan described below. At this time, please select appropriate datasets used to assess the effectiveness of this proposed method.

    Problem:
    {problem}

    Proposed Method:
    {proposed_method}

    Experimental Plan:
    {experiment_design}
    """
    prompt_spec = PromptBasedInstructionParser(task_type=TaskType.TEXT_GENERATION)
    prompt_spec._instruction = prompt_text
    dataset_retriever = DescriptionDatasetRetriever(
        max_search_depth=3  # TODO: とりあえずデータセット数は決め打ちで3にしてるけど可変にしたい
    )
    top_dataset_names = dataset_retriever.retrieve_top_datasets(prompt_spec)

    with open("dataset_names.txt") as f:
        f.write(top_dataset_names)

    return top_dataset_names


def select_models(problem: str, proposed_method: str, experiment_design: str) -> str:

    # 事前学習済みモデルの取得  TODO: ここ全部丸ごと抽象化しても良い
    prompt_text = f"""
    Task: You will verify the effectiveness of the proposed method that is expected to solve the following problem using the experimental plan described below. At this time, please select appropriate models as the baselines for comparison with this proposed method.

    Problem:
    {problem}

    Proposed Method:
    {proposed_method}

    Experimental Plan:
    {experiment_design}
    """
    prompt_spec = PromptBasedInstructionParser(task_type=TaskType.TEXT_GENERATION)
    prompt_spec._instruction = prompt_text
    model_retriever = DescriptionModelRetriever(
        model_descriptions_index_path="huggingface_data/huggingface_models/model_info/",
        use_bm25=True,
        use_HyDE=True,
        search_depth=3
    )
    top_model_names = model_retriever.retrieve(prompt_spec)

    with open("model_names.txt") as f:
        f.write(top_model_names)

    return top_model_names

if __name__ == "__main__":
    with open("research_problem.txt") as f:
        research_problem = f.read()
    with open("proposed_method.txt") as f:
        proposed_method = f.read()
    with open('experiment_design.txt'):
        experiment_design = f.read()
    dataset_names = select_data(research_problem, proposed_method, experiment_design)
    model_names = select_models(research_problem, proposed_method, experiment_design)
    print(dataset_names)
    print(model_names)