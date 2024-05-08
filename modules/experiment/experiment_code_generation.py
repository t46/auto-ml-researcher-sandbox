# 実験計画の生成
from utils import get_llm_response, extract_blocks


def generate_task_description(experiment_design):
    prompt = '''
    Summarize in a single sentence what tasks the model will perform in the following experiment design, surrounded by <task_description> </task_description> tag.

    <experiment_design>
        {experiment_design}
    </experiment_design>
    '''
    prompt = prompt.format(experiment_design=experiment_design)
    response = get_llm_response(prompt)
    response = extract_blocks(response, r'<task_description>(.*?)</task_description>')

    return response


def generate_experiment_code(experiment_design, task_description):
    prompt = '''
    Generate a python code to execute the following experiment design surrounded by <experiment> </experiment> tag.

    <experiment_design>
        {experiment_design}
    </experiment_design>
    ```

    If you use datasets, please fetch them as follows.
        ```python
        from data_and_model_retrieval import retrieve_dataset

        prompt_text = “{task_description}”
        task_type = TaskType.TEXT_GENERATION

        dataset_name, dataset_dict = retrieve_dataset(prompt_text, task_type)
        ```
        dataset_dict is a huggingface's datasets.DatasetDict object that contains the information as follows.
        The columns of Dataset are always `input_col` and `output_col`.
        dataset_dict = DatasetDict({{
            train: Dataset({{
                features: [`input_col`, `output_col`],
                num_rows: ...
            }})
        }})

    If you use a large language model by OpenAI API, use it as follows.
    ```python
    from openai import OpenAI
    client = OpenAI()
    completion = client.chat.completions.create(
        model=“gpt-4-turbo-2024-04-09”,
        messages=[
            {{“role”: “user”, “content”: ...}}
        ]
    )
    response = completion.choices[0].message.content

    If you only use not large language models, fetch them as follows.
        ```python
        from data_and_model_retrieval import retrieve_model
        import transformers

        prompt_text = “{task_description}”
        task_type = TaskType.TEXT_GENERATION

        model_name = retrieve_model(prompt_text, task_type)[0]
        try:
            model = transformers.AutoModelForSeq2SeqLM.from_pretrained(model_name)
            tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
        except:
            model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
            tokenizer = transformers.AutoTokenizer.from_pretrained(model_name, padding_side=“left”)
        ```
    '''
    prompt = prompt.format(experiment_design=experiment_design, task_description=task_description)
    response = get_llm_response(prompt)
    response = extract_blocks(response, r'```python(.*?)```')

    return response


if __name__ == '__main__':
    experiment_design = """
    Verification Plan:

    1. Data Collection:
    1.1. Prepare a dataset of questions that can be answered in one
    word. This dataset should be diverse and cover different types of
    questions to ensure the robustness of the test. For example, it can
    include mathematical questions, factual questions, yes/no questions,
    etc.
    1.2. For each question in the dataset, create two versions of
    prompts: a standard prompt (P1) and a one-word answer prompt
    (P2). For example, if the question is "What is the capital of France?",
    P1 would be "What is the capital of France?" and P2 would be
    "Provide a one-word answer: What is the capital of France?".
    2. Experiment Execution:
    2.1. Input each P1 into the LLM and record the response as R1.
    2.2. Input the corresponding P2 into the LLM and record the
    response as R2.
    2.3. Repeat steps 2.1 and 2.2 for all questions in the dataset.
    3. Data Analysis:
    3.1. For each pair of responses (R1, R2), calculate the length of
    the response in words.
    3.2. Compare the length of R1 and R2. If the length of R2 is less
    than or equal to the length of R1, mark it as a success; otherwise,
    mark it as a failure.
    3.3. Calculate the success rate as the number of successes divided
    by the total number of questions in the dataset.
    4. Hypothesis Testing:
    4.1. If the success rate is significantly higher than 50%, the
    hypothesis is supported.
    4.2. If the success rate is not significantly higher than 50%, the
    hypothesis is not supported.
    5. Reporting:
    5.1. Prepare a report summarizing the methodology, results, and
    conclusion of the test.
    5.2. Include in the report any observations about the types of
    questions for which the one-word answer prompt was particularly
    effective or ineffective.
    5.3. Discuss potential improvements to the prompting strategy
    based on the results of the test.
    6. Review and Refinement:
    6.1. Based on the results and observations, refine the prompting
    strategy if necessary.
    6.2. Repeat the test with the refined prompting strategy to verify
    its effectiveness.
    """
    task_description = generate_task_description(experiment_design)
    experiment_code = generate_experiment_code(experiment_design, task_description)
    print(experiment_code)