# 実験計画の生成

from utils import get_llm_response, extract_blocks

def generate_research_problem(goal):
    prompt = '''
    Your task is to generate the best research problem needed to be solved to achieve the following goal surrounded by <goal></goal> tags.
    - Generate the research problem by surrounding it with <problem></problem> tags.

    <goal>
        {goal}
    </goal>
    '''

    prompt = prompt.format(goal=goal)

    response = get_llm_response(prompt)

    response = extract_blocks(response, r'<problem>(.*?)</problem>')

    return response

if __name__ == '__main__':
    goal = """
    The goal is to resolve AI alignment problem. The AI alignment problem refers to the challenge of ensuring that artificial intelligence systems, 
    particularly those with advanced capabilities, act in ways that align with human values and intentions. 
    This issue has become more critical as AI systems have evolved from simple, task-specific programs to complex, 
    autonomous systems capable of making decisions without human intervention. 
    Modern AI, with advancements in machine learning and deep learning, can perform a wide range of tasks and analyze vast amounts of data, 
    making their behavior less predictable and harder to control. The problem arises from the difficulty in defining human values and goals precisely, 
    which can lead to unintended consequences even in well-intentioned AI systems. For instance, 
    an AI designed to maximize paperclip production might convert all available resources into paperclips, ignoring broader human context. 
    The complexity and opacity of AI decision-making, especially in deep learning systems, further complicate the alignment issue. 
    Ensuring these systems act in ways that are beneficial and aligned with human values is crucial for safety, trust, ethics, and the long-term impact of AI on society. 
    Misaligned AI systems could cause harm through unintended actions or conflicting objectives, and maintaining trust in AI technologies requires assurance that these systems will act beneficially. 
    Furthermore, as AI systems play increasingly significant roles in decision-making processes, integrating ethical considerations and ensuring they respect human rights and values is essential. 
    The AI alignment problem is a multifaceted challenge that necessitates collaboration across various disciplines to develop AI systems that are powerful, efficient, safe, trustworthy, and aligned with human values.
    """

    research_problem = generate_research_problem(goal)

    print(research_problem)