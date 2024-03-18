from openai import OpenAI
import re

with open('formulated_proposed_method.txt', 'r') as f:
    proposed_method = f.read()

prompt = f"""

Translate the following proposed method into Python code. Use your best judgment to implement any parts that are unclear. If implementing a neural network, use PyTorch.

Proposed Method:
{proposed_method}
"""

# TODO: OpenAI の返答を生成する部分を関数・メソッド化する

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

prompt = f"""
Please regenerate the Python code, including any parts that remain as follows:

Only comments are written without any implementation.
Only placeholders are implemented.
Left unimplemented as TODOs.

Python Code:
{response.choices[0].message.content}
"""

# TODO: utils などに移動する
def extract_python_blocks(text):
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    combined = '\n'.join(match.strip() for match in matches)
    return combined

code = extract_python_blocks(response.choices[0].message.content)

with open('proposed_method.py', 'w') as f:
    f.write(code)


print(code)