# 実験計画の生成

from utils import get_llm_response, extract_blocks

def generate_solution_hypotheses(problem):
    prompt = '''
    Your task is to generate the best solution ideas to solve the following problem.
    Generate multiple candidates for ideas of solutions to solve the following problem, enclosed in <approach_candidates></approach_candidates> tags.
    - The solutions must be able to solve the problem in a general way, not just for specific cases.
    - The solutions must be concrete and specific, not abstract or vague.
    - The solutions must be something that no one has realized before.

    <problem>
        {problem}
    </problem>
    '''

    prompt = prompt.format(problem=problem)

    response = get_llm_response(prompt)

    response = extract_blocks(response, r'<approach_candidates>(.*?)</approach_candidates>')

    return response

def select_solution_hypothesis(approach_candidates):
    prompt = '''
    Your task is to select the best solution idea among the following candidates.
    Select the best solution idea from the following candidates and output it by enclosing in <approach></approach> tags.
    - The solution should be the easiest to implement and evaluate.
    - The solution shoule be able to be implemented in a short period of time.
    - The solution shoule be able to be implemented by a machine or computer.

    <approach_candidates>
        {approach_candidates}
    </approach_candidates>
    '''

    prompt = prompt.format(approach_candidates=approach_candidates)

    response = get_llm_response(prompt)

    response = extract_blocks(response, r'<approach>(.*?)</approach>')

    return response

if __name__ == '__main__':
    problem = """
    Background:
    We use a Large Language Model (LLM), specifically GPT-4, which
    takes any text as input and outputs text in response. We input
    instructions, called prompts, to the LLM, and the LLM generates text
    based on those instructions.
    Problem:
    The issue is that the large language model may output sentences not
    directly related to the instructions.
    For example, if you enter the sentence "What is 1 + 1?" into the LLM,
    it will often respond with "The answer to that question is 2." In this
    response, what we really want is just the "2" part. The sentence "The
    answer to that question is" is extraneous, and we would prefer the
    LLM to output only the part that directly related to the question, "2".
    The reason this is problematic is that we must perform postprocessing to evaluate the output. For instance, if you want to
    evaluate the LLM's performance on a dataset of math problems, and
    a sample is a question "What is 1 + 1?" paired with the correct
    answer "2", we must check whether the LLM's answer matches "2". If
    the LLM outputs an extra sentence besides "2," even if the answer is
    actually correct, it may be judged as incorrect due to the apparent
    mismatch.
    It is challenging to address this issue with a predefined postprocessing method, as it is not known in advance what kind of
    extraneous text will be output.
    To sum up, the problems are as follows:
    - The large language model outputs sentences that are not directly
    related to the instructions.
    - Predefined post-processing methods are problem/answer-specific
    and not general.
    """

    approach_candidates = generate_solution_hypotheses(problem)
    approach = select_solution_hypothesis(approach_candidates)

    print(approach)