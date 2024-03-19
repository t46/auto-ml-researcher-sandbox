from openai import OpenAI

def generate_experiment_design(problem: str, proposed_method: str, client: OpenAI) -> str:

    prompt = f"""
    Design an experimental plan to verify the effectiveness of the proposed method for solving the problem described below.

    Problem:
    {problem}

    Proposed Method:
    {proposed_method}
    """

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0.0,
        messages=[{"role": "user", "content": prompt},
                {"role": "system", "content": "You are a machine learning researcher."}],
        )

    with open('experiment_design.txt', 'w') as f:
        f.write(response.choices[0].message.content)

    return response.choices[0].message.content

if __name__ == "__main__":
    client = OpenAI()
    with open("research_problem.txt") as f:
        research_problem = f.read()
    with open("proposed_method.txt") as f:
        proposed_method = f.read()
    experiment_design = generate_experiment_design(research_problem, proposed_method, client)
    print(experiment_design)

