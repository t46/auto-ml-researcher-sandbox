from openai import OpenAI

prompt = """
Below, I present an issue, a proposed method for solving it, and an experimental plan to validate the effectiveness of this method. Please generate Python code to execute this experimental plan. However, strictly follow the instructions below:

When using a baseline model and dataset for validation, please use the following model and dataset provided by Huggingface:
Dataset: {dataset_names}
Model: {model_names}
Do not specify the API Key in the Python code
Do not leave any TODOs or placeholders that assume implementation at a later stage

Issue:
{issue} ← Insert information about the issue here.

Proposed Method:
{proposed_method} ← Insert information about 1. Implementation of the proposed method, 2. Where it is saved, or 3. How to use it here.

Experimental Design:
{experimental_design}
"""

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

print(response.choices[0].message.content)