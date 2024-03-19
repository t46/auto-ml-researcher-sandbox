from openai import OpenAI

def generate_proposed_method(problem: str, client: OpenAI) -> str:


    prompt = f"""
    Generate the best idea to solve the problem described below.

    Problem:
    {problem}
    """

    # TODO: OpenAI の返答を生成する部分を関数・メソッド化する
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

    return response.choices[0].message.content


if __name__ == "__main__":
    client = OpenAI()
    with open("./research_problem.txt") as f:
        research_problem = f.read()
    proposed_method = generate_proposed_method(research_problem, client)
    print(proposed_method)