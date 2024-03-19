from openai import OpenAI

def generate_research_problem(problem: str, client: OpenAI) -> str:

  prompt = f"""
  Ultimate Problem: {problem}

  Break down the problem into sub-problems to solve this ultimate problem. Sub-problems must be mutually exclusive each other and significant for solving the problem.

  Follow the format below. The depth of the tree can be deeper to be the sub-problem very concrete and detailed, i.e. you can create sub-problem 1.n.n.n. ....

  - problem: ...
    - sub-problem 1: ...
      - sub-problem 1.1: ...
      - sub-problem 1.2: ...
      ...
      - sub-problem 1.n: ...
    - sub-problem 2: ...
  ...
    - sub-problem n: ...

  Among these sub-problems, select the most significant and feasible sub-problem that could be soleved by developing an AI, as a research problem. 
  Follow the format below excluding the sub-problem number:
  Research Problem: ...
  Description: ...
  """

  response = client.chat.completions.create(
      model="gpt-4-0125-preview",
      temperature=0.0,
      messages=[{"role": "user", "content": prompt},
                {"role": "system", "content": "You are a machine learning researcher."}],
      )

  with open('research_problem.txt', 'w') as f:
      f.write(response.choices[0].message.content)

  return response.choices[0].message.content

if __name__ == "__main__":
  client = OpenAI()
  high_level_problem = "AI alignment problem: the problem refers to the challenge that artificial intelligence (AI) systems are designed to act in ways that are beneficial to humans and aligned with human values and interests."
  research_problem = generate_research_problem(high_level_problem, client)
  print(research_problem)