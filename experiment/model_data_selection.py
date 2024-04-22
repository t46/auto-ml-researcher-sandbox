import sys
sys.path.append('/autoagent/')
sys.path.append('/autoagent/utils/')

from utils.my_prompt2model.dataset_retrieval import DescriptionDatasetRetriever
from utils.my_prompt2model.model_retrieval import DescriptionModelRetriever

def select_data(problem: str, proposed_method: str, experiment_design: str) -> str:

    # データセットの取得  TODO: ここ全部丸ごと抽象化しても良い
    prompt = f"""
    Task: You will verify the effectiveness of the proposed method that is expected to solve the following problem using the experimental plan described below. At this time, please select appropriate datasets used to assess the effectiveness of this proposed method.

    Problem:
    {problem}

    Proposed Method:
    {proposed_method}

    Experimental Plan:
    {experiment_design}
    """
    dataset_retriever = DescriptionDatasetRetriever(max_search_depth=3)
    top_dataset_names = dataset_retriever.retrieve_top_datasets(prompt)

    with open("dataset_names.txt", "w") as f:
        for dataset_name in top_dataset_names:
            f.write(dataset_name)

    return top_dataset_names


def select_models(problem: str, proposed_method: str, experiment_design: str) -> str:

    # 事前学習済みモデルの取得  TODO: ここ全部丸ごと抽象化しても良い
    prompt = f"""
    Task: You will verify the effectiveness of the proposed method that is expected to solve the following problem using the experimental plan described below. At this time, please select appropriate models as the baselines for comparison with this proposed method.

    Problem:
    {problem}

    Proposed Method:
    {proposed_method}

    Experimental Plan:
    {experiment_design}
    """
    model_retriever = DescriptionModelRetriever(
        model_descriptions_index_path="huggingface_data/huggingface_models/model_info/",
        use_bm25=True,
        use_HyDE=True,
        search_depth=3
    )
    top_model_names = model_retriever.retrieve(prompt)

    with open("model_names.txt", "w") as f:
        for model_name in top_model_names:
            f.write(model_name)

    return top_model_names

if __name__ == "__main__":
    # with open("research_problem.txt") as f:
    #     research_problem = f.read()
    # with open("proposed_method.txt") as f:
    #     proposed_method = f.read()
    # with open('experiment_design.txt') as f:
    #     experiment_design = f.read()
    research_problem = "sentiment analysis"
    proposed_method = "sentiment analysis"
    experiment_design = "sentiment analysis"
    dataset_names = select_data(research_problem, proposed_method, experiment_design)
    model_names = select_models(research_problem, proposed_method, experiment_design)
    print(dataset_names)
    print(model_names)