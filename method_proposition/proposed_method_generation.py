from openai import OpenAI

prompt = """
Generate the best idea to solve the problem described below.

Problem:
{problem}
"""

# TODO: OpenAI の返答を生成する部分を関数・メソッド化する

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

with open('proposed_method.txt', 'w') as f:
    f.write(response.choices[0].message.content)


prompt = f"""
Formulate the following proposed method mathematically.

Proposed Method:
{response.choices[0].message.content}
"""

response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

prompt = f"""
Further concretize and formalize the following proposed method and regenerate the updated proposed method.

Proposed Method:
{response.choices[0].message.content}
"""

response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

with open('formulated_proposed_method.txt', 'w') as f:
    f.write(response.choices[0].message.content)

print(response.choices[0].message.content)