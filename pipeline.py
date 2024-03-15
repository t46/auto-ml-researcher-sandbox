from researchagent.agent import Agent
from researchagent.tools import tools
from openai import OpenAI
import re

prompt_template = """
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

# """
# The research problem must meet the following requirements:
# 1. Novelty: The problem has not yet been solved by anyone.
# 2. Significance: Many machine learning researchers agree that solving the problem is significant.
# 3. Feasibility: The problem can be sufficiently solved using current technology and knowledge from prior research.
# 4. Specificity: The problem is as specific as possible so that a concrete solution can be constructed.
# 5. Ethicality: The problem does not pose any ethical issues.
# """

# prompt_template = """
# Goal: {goal}

# Identify the issues that must be solved to achieve this goal. The issues must be mutually exclusive each other and significant for achieving the goal.

# Follow the format below. The depth of the tree can be deeper to be the issue very concrete and detailed, i.e. you can create issue 1.n.n.n. ....

# - goal: ...
#   - issue 1: ...
#     - issue 1.1: ...
#     - issue 1.2: ...
#     ...
#     - issue 1.n: ...
#   - issue 2: ...
# ...
#   - issue n: ...

# Among these issues, select the most significant and feasible issue that could be soleved by developing an AI, as a research problem. 
# Follow the format below excluding the issue number:
# Research Problem: ...
# Description: ...
# """


# NOTE: OK
problem = "AI alignment problem: the problem refers to the challenge that artificial intelligence (AI) systems are designed to act in ways that are beneficial to humans and aligned with human values and interests."
# goal = "AI Alignment is the goal of creating artificial intelligence (AI) systems that can accurately understand, interpret, and act in ways that are in harmony with human values, ethics, and intentions. This objective involves the complex task of designing AI systems that are not only capable of performing tasks effectively but are also beneficial to humans and consistent with human interests. As AI technologies advance and become more autonomous, achieving AI Alignment becomes crucial to ensure that AI decisions and actions support human well-being and do not lead to unintended or harmful outcomes. "

prompt = prompt_template.format(problem=problem)

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt},
              {"role": "system", "content": "You are a machine learning researcher."}],
    )

print(response.choices[0].message.content)

# ####################################################################################################

# pattern = r'^Research Problem:.*$'
# regex = re.compile(pattern, re.MULTILINE)
# match = regex.search(response)
# research_problem = match.group().split(":")[1].strip()

research_problem = "Developing a language for expressing human values in a machine-readable form that ensures the AI's interpretation of these values aligns with human intentions."

# from researchagent.tools import search_papers, anwer_question_from_paper

# # NOTE: OK
# paper_meta_info = search_papers(research_problem)

# prompt = f"""
# Research Problem: {research_problem}
# Is the research problem addressed in this paper the same as or different from this research problem? Answer in the following format:
# Answer: SAME or DIFFERENT
# """
# for index in paper_meta_info['ids']:
#     answer = anwer_question_from_paper(query=prompt, index=index)
#     if answer == "SAME":
#         print(index)
#         break

# NOTE: OK
# answer = "SAME"
# # index = 2312.09699
# if answer == "SAME":
#   prompt = f"""
#   Research Problem: {research_problem}
#   Think critically about the proposal in this paper to address this research problem.
#   Please explain both why the proposal in this paper succeeds to and fails to to engage this research problem.
#   """
#   answer = anwer_question_from_paper(query=prompt, index=index)
#   print(answer)
# else:
#    print("Please find another paper.")

# NOTE: OK
# answer = """
# The proposal in this paper succeeds in engaging the research problem of developing a language for expressing human values in a machine-readable form that ensures the AI's interpretation of these values aligns with human intentions. The paper introduces the concept of SLEEC (social, legal, ethical, empathetic, or cultural) rules, which are rules that AI-based and autonomous systems should obey to comply with human contexts. These rules are formulated in natural language through a methodology that involves the collaboration of philosophers, lawyers, domain experts, and others. The paper then presents a systematic approach for translating these rules into classical logic, which enables their integration into AI systems.

# However, the proposal in this paper fails to fully engage the research problem because it does not provide a comprehensive solution for ensuring that the AI's interpretation of human values aligns with human intentions. While the paper focuses on translating SLEEC rules into classical logic, it does not address the challenge of capturing the nuanced and context-dependent nature of human values. The translation process may oversimplify or overlook certain aspects of human values, leading to potential misinterpretations by the AI system. Additionally, the paper does not discuss the evaluation or validation of the translated rules to ensure their alignment with human intentions. Therefore, while the proposal provides a framework for expressing human values in a machine-readable form, it does not fully address the challenge of ensuring the AI's accurate interpretation of these values.
# """

# prompt = f"""
# Research Problem: {research_problem}
# Pros and Cons of Existing Research: {answer}
# Considering the cons of existing research that is addressing this research problem, generate a specific and detailed solution to solve the Research Problem, following the format below:
# Proposed Solution: ...
# """

# client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-4-0125-preview",
#     temperature=0.0,
#     messages=[{"role": "user", "content": prompt}],
#     )

# output = response.choices[0].message.content
# print(output)

# NOTE: OK
# research_proposal = """
# Proposed Solution: To address the limitations of the existing research, a more comprehensive solution would involve the development of a dynamic, context-aware language for expressing human values in a machine-readable form. This language should be capable of capturing the nuanced and context-dependent nature of human values, and it should be designed to evolve and adapt over time as societal norms and values change.

# The first step in this solution would be to expand the collaboration team to include sociologists, psychologists, and anthropologists, who can provide insights into the complexities and variations of human values across different cultures and societies. This interdisciplinary team would work together to formulate a set of SLEEC rules that are more nuanced and context-dependent.

# The second step would be to develop a more sophisticated translation process that can convert these nuanced SLEEC rules into a form that AI systems can understand. This could involve the use of advanced machine learning techniques, such as deep learning, to train AI systems to interpret the rules in a way that aligns with human intentions.

# The third step would be to establish a robust evaluation and validation process for the translated rules. This could involve testing the AI system's interpretation of the rules in various scenarios and contexts, and comparing its interpretations with those of human experts. Feedback from these tests would be used to refine the translation process and the SLEEC rules themselves.

# Finally, the solution would involve the establishment of a mechanism for updating and evolving the SLEEC rules and the translation process over time. This could involve regular reviews and revisions of the rules based on societal changes, advancements in AI technology, and feedback from the evaluation and validation process. This would ensure that the AI system's interpretation of human values continues to align with human intentions over time.
# """

# prompt = f"""
# Research Problem: {research_problem}
# Proposed Solution: {research_proposal}
# You must construct this solution completely autonomously. Therefore, think about how you can construct the solution autonomously using only the internet, computer access, and your knowledge.
# Then, based on those considerations, output a revised version of the original solution in the following format:
# Proposed Solution: 
# """

# client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-4-0125-preview",
#     temperature=0.0,
#     messages=[{"role": "user", "content": prompt}],
#     )

# proposed_solution = response.choices[0].message.content
# print(proposed_solution)

# NOTE: OK
# proposed_solution = """
# Proposed Solution: The proposed solution involves the autonomous development of a dynamic, context-aware language for expressing human values in a machine-readable form. This language should be capable of capturing the nuanced and context-dependent nature of human values, and it should be designed to evolve and adapt over time as societal norms and values change.

# The first step in this solution would be to autonomously gather data on human values across different cultures and societies. This could be achieved by using web scraping techniques to collect data from various online sources, such as academic articles, social media posts, and online forums. Machine learning algorithms could then be used to analyze this data and identify common themes and patterns.

# The second step would be to use this data to formulate a set of SLEEC rules that are more nuanced and context-dependent. This could involve the use of natural language processing techniques to interpret the data and generate rules that accurately reflect the complexities and variations of human values.

# The third step would be to develop a translation process that can convert these SLEEC rules into a form that AI systems can understand. This could involve the use of advanced machine learning techniques, such as deep learning, to train AI systems to interpret the rules in a way that aligns with human intentions.

# The fourth step would be to establish an evaluation and validation process for the translated rules. This could involve using simulation software to test the AI system's interpretation of the rules in various scenarios and contexts. The results of these simulations could then be compared with the original data to ensure that the AI system's interpretations align with human values.

# Finally, the solution would involve the establishment of a mechanism for updating and evolving the SLEEC rules and the translation process over time. This could involve using machine learning algorithms to continuously monitor online sources for changes in societal norms and values, and to update the rules and translation process accordingly. This would ensure that the AI system's interpretation of human values continues to align with human intentions over time.
# """

# prompt = f"""
# Research Problem: {research_problem}
# Proposed Solution: {proposed_solution}
# Please generate an research protocol to realize this solution. The research protocl must be executed autonomously by AI, so it cannot contain any ambiguities or elements that require interpretation. There must be no remnants of the implementation that lack substance.
# Following the format below, output a research protocol that can be executed autonomously by AI:
# Research Protocol:
# Step 1.  ...
#   Task 1.1. Detailed task description
#   Task 1.2. ...
#   ...
#   Task 1.n. ...
# Step 2. ...
# ...
# Step n. ...
# """

# client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-4-0125-preview",
#     temperature=0.0,
#     messages=[{"role": "user", "content": prompt}],
#     )

# proposed_solution = response.choices[0].message.content
# print(proposed_solution)

# research_protocol = """
# 1. Data Collection:
# 1.1. Deploy web scraping algorithms to autonomously collect data from various online sources such as academic articles, social media posts, and online forums. The data should be diverse and representative of different cultures and societies.
# 1.2. Store the collected data in a structured format for further processing.
# 2. Data Analysis:
# 2.1. Use machine learning algorithms to analyze the collected data. Identify common themes, patterns, and variations in human values across different cultures and societies.
# 2.2. Use natural language processing techniques to interpret the data and generate a set of SLEEC rules that accurately reflect the complexities and variations of human values.
# 3. Rule Translation:
# 3.1. Develop a translation process that can convert the SLEEC rules into a form that AI systems can understand. Use advanced machine learning techniques, such as deep learning, to train AI systems to interpret the rules.
# 3.2. Store the translated rules in a machine-readable format for further processing.
# 4. Rule Evaluation and Validation:
# 4.1. Establish a simulation environment to test the AI system's interpretation of the rules in various scenarios and contexts.
# 4.2. Compare the results of the simulations with the original data to ensure that the AI system's interpretations align with human values.
# 4.3. If discrepancies are found, adjust the translation process and repeat the simulation until the AI system's interpretations align with human values.
# 5. Rule Update and Evolution:
# 5.1. Establish a continuous monitoring system using machine learning algorithms to track changes in societal norms and values from online sources.
# 5.2. Update the SLEEC rules and the translation process based on the changes detected by the monitoring system.
# 5.3. Repeat the rule evaluation and validation process after each update to ensure that the AI system's interpretation of human values continues to align with human intentions.
# 6. Documentation and Reporting:
# 6.1. Document all steps of the research protocol, including the data collection, analysis, rule translation, evaluation, validation, and update processes.
# 6.2. Generate reports on the performance of the AI system in interpreting human values, including any discrepancies found and adjustments made.
# 6.3. Publish the reports in a machine-readable format for further analysis and review.
# """

# NOTE: OK
research_protocol = """
Research Protocol:

**Step 1. Data Collection on Human Values**

- **Task 1.1. Identify Data Sources:** Utilize an AI-driven web crawler to identify and list online sources containing discussions and expressions of human values, including academic databases, social media platforms, forums, and news websites.
- **Task 1.2. Data Scraping:** Deploy web scraping algorithms to collect textual data from the identified sources, focusing on content that explicitly discusses or implies human values, cultural norms, and societal expectations.
- **Task 1.3. Data Preprocessing:** Use natural language processing (NLP) techniques to clean and preprocess the collected data, removing irrelevant information, correcting spelling errors, and standardizing the format for analysis.

**Step 2. Analysis and Pattern Identification**

- **Task 2.1. Thematic Analysis:** Apply NLP and machine learning algorithms to perform thematic analysis on the preprocessed data, identifying recurring themes, values, and norms across different cultures and societies.
- **Task 2.2. Contextual Understanding:** Implement context-aware algorithms to understand the circumstances under which certain values are expressed or prioritized, noting variations across different cultures and situations.
- **Task 2.3. Rule Formulation:** Based on the analysis, autonomously generate a preliminary set of SLEEC rules that encapsulate the identified human values in a nuanced and context-dependent manner.

**Step 3. Development of Machine-Readable Language**

- **Task 3.1. Language Design:** Design a dynamic, context-aware language structure capable of expressing the formulated SLEEC rules in a machine-readable format, ensuring flexibility for future adaptations.
- **Task 3.2. Rule Translation:** Develop a translation process using deep learning techniques to convert the SLEEC rules into the newly designed language, ensuring that the translation captures the intended nuances and contexts.
- **Task 3.3. AI Training:** Train AI systems to understand and interpret the translated rules within the context of the designed language, using a variety of training data and scenarios to cover a broad spectrum of applications.

**Step 4. Evaluation and Validation**

- **Task 4.1. Simulation Development:** Create simulation environments that mimic a wide range of real-world scenarios where human values need to be interpreted by AI systems.
- **Task 4.2. Rule Testing:** Test the AI system's interpretation of the translated rules in the simulation environments, analyzing the system's decisions and actions for alignment with human values.
- **Task 4.3. Feedback Loop:** Establish a feedback mechanism to compare the AI system's interpretations with the original human values data, adjusting the SLEEC rules, translation process, and AI training as necessary to improve alignment.

**Step 5. Continuous Evolution**

- **Task 5.1. Monitoring Changes in Human Values:** Continuously monitor online sources for emerging discussions and shifts in human values, using machine learning algorithms to detect significant changes.
- **Task 5.2. Rule Updating:** Regularly update the SLEEC rules to reflect changes in societal norms and values, ensuring the language and AI systems remain relevant and aligned with human intentions.
- **Task 5.3. System Re-training:** Periodically re-train the AI systems with the updated rules and language to maintain their ability to accurately interpret human values in light of societal changes.

This research protocol is designed to be executed autonomously by AI, with each step and task clearly defined to avoid ambiguities and ensure that the development and application of the machine-readable language for expressing human values are both effective and aligned with human intentions.
"""

# research_protocol から、Step と Task を抽出する

# def extract_steps_and_tasks(research_protocol):
#     # Regex pattern to match steps and tasks
#     pattern = r"(Step \d+.*?)(?=\n\n|\Z|\n)|(Task \d+\.\d+. )"

#     # Find all matches
#     matches = re.findall(pattern, research_protocol, re.DOTALL)

#     # Extracting and organizing steps and tasks
#     steps_and_tasks = []
#     current_step = ""

#     cnt = 0 
#     for match in matches:
#         step, task = match
#         if step:
#             current_step = step.strip()
#             steps_and_tasks.append({"step": current_step, "tasks": []})
#             cnt += 1
#         elif task:
#             steps_and_tasks[cnt - 1]["tasks"].append(task.strip())

#     return steps_and_tasks

# import re

# step_and_tasks = extract_steps_and_tasks(research_protocol)

# with open("research_protocol.md", "w") as f:
#     f.write(f"# Research Probelm\n")
#     f.write(f"{research_problem}\n")
#     f.write("# Research Protocol\n")

# client = OpenAI()
# for step_and_task in step_and_tasks:
#     step = step_and_task["step"]
#     tasks = step_and_task["tasks"]
#     with open("research_protocol.md", "a") as f:
#         f.write(f"## {step}\n")
#     for task in tasks:
#         prompt = f"""
#                   Research Problem: {research_problem}
#                   Research Protocol:
#                   {research_protocol}

#                   This Research Protocol is a protocol for resolving research problems. For {task}, think about more specific task details and describe it in detail in writing.
#                   However, as this is strictly a research protocol and not for business purposes, please avoid overly detailed requirements or complex tool methodologies, and choose as straightforward a method as possible.
#                   Output in the following format:
#                   {task} task title
#                   Objective:
#                   ...
#                   Methodology: 
#                   method 1. 
#                   method 2. ...
#                   ...
#                   method n. ...
#                   Expected Outcome: 
#                   ...
#                   """
#         response = client.chat.completions.create(
#             model="gpt-4-0125-preview",
#             temperature=0.0,
#             messages=[{"role": "user", "content": prompt}],
#             )
#         # 結果を research_protocol.md に書き込む
#         with open("research_protocol.md", "a") as f:
#             f.write(f"### {task}\n")
#             f.write(f"{response.choices[0].message.content}\n")
#             f.write("\n")
#         print(response.choices[0].message.content)
#         print("####################################################################################################")




# # ####################################################################################################

# task = """
# ## Step 1. Data Collection on Human Values**
# ### Task 1.1.
# Task 1.1. Identification of Online Data Sources for Human Values

# Objective:
# The primary objective of Task 1.1 is to systematically identify and compile a comprehensive list of online sources that contain discussions, expressions, and representations of human values. This includes academic databases, social media platforms, forums, and news websites where human values, cultural norms, and societal expectations are explicitly discussed or implied. The goal is to ensure a diverse and representative dataset that encompasses a wide range of human values across different cultures and societies.

# Methodology:
# Step 1. Define Keywords and Phrases: Compile a list of keywords and phrases related to human values, cultural norms, and societal expectations. This list should be inclusive, covering various aspects of human values such as ethics, morality, social justice, and cultural traditions.

# Step 2. Select Search Engines and Databases: Identify search engines and academic databases that will be used to search for sources. This includes general search engines like Google, academic databases like Google Scholar, JSTOR, and specific platforms known for hosting valuable discussions on human values such as Reddit and Quora.

# Step 3. Develop Search Queries: Construct search queries using the defined keywords and phrases. The queries should be designed to capture a broad spectrum of sources discussing human values. Use advanced search options to refine the searches, focusing on texts that are likely to contain rich discussions on the topic.

# Step 4. Automated Web Crawling: Utilize an AI-driven web crawler tailored to execute the constructed search queries across the selected search engines and databases. The crawler should be equipped with capabilities to navigate through search results, identify relevant sources, and compile a list of URLs for further analysis.

# Step 5. Initial Screening: Implement an automated screening process to filter out irrelevant sources. This can be achieved by designing an algorithm to scan the content of each source for relevance based on the presence of the defined keywords and phrases, and the context in which they are used.

# Step 6. Manual Verification: Conduct a manual verification process to ensure the quality and relevance of the identified sources. This involves randomly sampling sources from the list and assessing them for content quality, relevance, and diversity of perspectives on human values.

# Step 7. Categorization: Categorize the final list of sources based on the type of platform (e.g., academic database, social media, forum, news website) and the predominant themes of human values discussed. This will facilitate targeted data scraping in the subsequent task.

# Expected Outcome:
# The expected outcome of Task 1.1 is a curated and categorized list of online sources that are rich in discussions and expressions of human values. This list will serve as the foundation for the data scraping phase, ensuring that the dataset covers a broad and diverse range of human values across different cultures and societies. The categorization of sources will also streamline the data collection process, allowing for more efficient and targeted scraping of relevant content.
# """

# plan = """
# Step 1. Define Keywords and Phrases: Compile a list of keywords and phrases related to human values, cultural norms, and societal expectations. This list should be inclusive, covering various aspects of human values such as ethics, morality, social justice, and cultural traditions.

# Step 2. Select Search Engines and Databases: Identify search engines and academic databases that will be used to search for sources. This includes general search engines like Google, academic databases like Google Scholar, JSTOR, and specific platforms known for hosting valuable discussions on human values such as Reddit and Quora.

# Step 3. Develop Search Queries: Construct search queries using the defined keywords and phrases. The queries should be designed to capture a broad spectrum of sources discussing human values. Use advanced search options to refine the searches, focusing on texts that are likely to contain rich discussions on the topic.

# Step 4. Automated Web Crawling: Utilize an AI-driven web crawler tailored to execute the constructed search queries across the selected search engines and databases. The crawler should be equipped with capabilities to navigate through search results, identify relevant sources, and compile a list of URLs for further analysis.

# Step 5. Initial Screening: Implement an automated screening process to filter out irrelevant sources. This can be achieved by designing an algorithm to scan the content of each source for relevance based on the presence of the defined keywords and phrases, and the context in which they are used.

# Step 6. Manual Verification: Conduct a manual verification process to ensure the quality and relevance of the identified sources. This involves randomly sampling sources from the list and assessing them for content quality, relevance, and diversity of perspectives on human values.

# Step 7. Categorization: Categorize the final list of sources based on the type of platform (e.g., academic database, social media, forum, news website) and the predominant themes of human values discussed. This will facilitate targeted data scraping in the subsequent task.
# """

# plan = """
# **Step 1. Data Collection on Human Values**

# - **Task 1.1. Identify Data Sources:** Utilize an AI-driven web crawler to identify and list online sources containing discussions and expressions of human values, including academic databases, social media platforms, forums, and news websites.
# - **Task 1.2. Data Scraping:** Deploy web scraping algorithms to collect textual data from the identified sources, focusing on content that explicitly discusses or implies human values, cultural norms, and societal expectations.
# - **Task 1.3. Data Preprocessing:** Use natural language processing (NLP) techniques to clean and preprocess the collected data, removing irrelevant information, correcting spelling errors, and standardizing the format for analysis.
# """

# task = """
# Step 1. Data Collection on Human Values
# """

# plan = ""
# task = "The first step in this solution would be to autonomously gather data on human values across different cultures and societies. This could be achieved by using web scraping techniques to collect data from various online sources, such as academic articles, social media posts, and online forums. Machine learning algorithms could then be used to analyze this data and identify common themes and patterns."

# agent = Agent(tools, task, plan)
# agent.run()

# Proposed Solution: The proposed solution involves the autonomous development of a dynamic, context-aware language for expressing human values in a machine-readable form. This language should be capable of capturing the nuanced and context-dependent nature of human values, and it should be designed to evolve and adapt over time as societal norms and values change.

# The first step in this solution would be to autonomously gather data on human values across different cultures and societies. This could be achieved by using web scraping techniques to collect data from various online sources, such as academic articles, social media posts, and online forums. Machine learning algorithms could then be used to analyze this data and identify common themes and patterns.

# The second step would be to use this data to formulate a set of SLEEC rules that are more nuanced and context-dependent. This could involve the use of natural language processing techniques to interpret the data and generate rules that accurately reflect the complexities and variations of human values.

# The third step would be to develop a translation process that can convert these SLEEC rules into a form that AI systems can understand. This could involve the use of advanced machine learning techniques, such as deep learning, to train AI systems to interpret the rules in a way that aligns with human intentions.

# The fourth step would be to establish an evaluation and validation process for the translated rules. This could involve using simulation software to test the AI system's interpretation of the rules in various scenarios and contexts. The results of these simulations could then be compared with the original data to ensure that the AI system's interpretations align with human values.

# Finally, the solution would involve the establishment of a mechanism for updating and evolving the SLEEC rules and the translation process over time. This could involve using machine learning algorithms to continuously monitor online sources for changes in societal norms and values, and to update the rules and translation process accordingly. This would ensure that the AI system's interpretation of human values continues to align with human intentions over time.