from openai import OpenAI

prompt = """
Design an experimental plan to verify the effectiveness of the proposed method for solving the problem described below.

Problem:
{problem}

Proposed Method:
{proposed_method}
"""

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

with open('experiment_design.txt', 'w') as f:
    f.write(response.choices[0].message.content)

print(response.choices[0].message.content)