from openai import OpenAI
import re


def get_llm_response(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[
            {"role": "system", "content": "You are a machine learning researcher."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def extract_blocks(text, pattern):
    matches = re.findall(pattern, text, re.DOTALL)
    return '\n'.join(match.strip() for match in matches)