from openai import OpenAI
import re

def generate_experiment_code(problem: str, proposed_method: str, experiment_design: str, dataset_names: str, model_names: str, client: OpenAI):

    prompt = f"""
    Below, I present an issue, a proposed method for solving it, and an experimental plan to validate the effectiveness of this method. Please generate Python code to execute this experimental plan. However, strictly follow the instructions below:

    When using a baseline model and dataset for validation, please use the following model and dataset provided by Huggingface:
    Dataset: {dataset_names}
    Model: {model_names}
    Do not specify the API Key in the Python code
    Do not leave any TODOs or placeholders that assume implementation at a later stage

    Problem:
    {problem}

    Proposed Method:
    {proposed_method}

    Experimental Design:
    {experiment_design}
    """

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0.0,
        messages=[{"role": "user", "content": prompt},
                {"role": "system", "content": "You are a machine learning researcher."}],
        )

    def extract_python_blocks(text):
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        combined = '\n'.join(match.strip() for match in matches)
        return combined

    code = extract_python_blocks(response.choices[0].message.content)
    with open('experiment_code.py', 'w') as f:
        f.write(code)

    return code

if __name__ == "__main__":
    client = OpenAI()
    with open("research_problem.txt") as f:
        research_problem = f.read()
    with open("proposed_method.txt") as f:
        proposed_method = f.read()
    with open('experiment_design.txt'):
        experiment_design = f.read()
    with open('dataset_names.txt'):
        dataset_names = f.read()
    with open('model_names.txt'):
        model_names = f.read()
    experiment_design_code = generate_experiment_code(research_problem, proposed_method, experiment_design, dataset_names, model_names, client)
    print(experiment_design_code)