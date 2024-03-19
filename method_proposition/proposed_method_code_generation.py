from openai import OpenAI
from utils.post_process import extract_python_blocks

def generate_proposed_method_code(proposed_method: str, client: OpenAI) -> str:

    prompt = f"""

    Translate the following proposed method into Python code. Use your best judgment to implement any parts that are unclear. If implementing a neural network, use PyTorch.

    Proposed Method:
    {proposed_method}
    """

    # TODO: OpenAI の返答を生成する部分を関数・メソッド化する

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

    code = extract_python_blocks(response.choices[0].message.content)

    with open('proposed_method.py', 'w') as f:
        f.write(code)

    return code

if __name__ == "__main__":
    client = OpenAI()
    with open('formulated_proposed_method.txt', 'r') as f:
        proposed_method = f.read()
    proposed_method_code = generate_proposed_method_code(proposed_method, client)
    print(proposed_method_code)