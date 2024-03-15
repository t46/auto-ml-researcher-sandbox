from openai import OpenAI

research_problem = "Research Problem: Developing a language for expressing human values in a machine-readable form that ensures the AI's interpretation of these values aligns with human intentions."

pros_cons_of_previous_study = """
The proposal in this paper succeeds in engaging the research problem of developing a language for expressing human values in a machine-readable form that ensures the AI's interpretation of these values aligns with human intentions. The paper introduces the concept of SLEEC (social, legal, ethical, empathetic, or cultural) rules, which are rules that AI-based and autonomous systems should obey to comply with human contexts. These rules are formulated in natural language through a methodology that involves the collaboration of philosophers, lawyers, domain experts, and others. The paper then presents a systematic approach for translating these rules into classical logic, which enables their integration into AI systems.

However, the proposal in this paper fails to fully engage the research problem because it does not provide a comprehensive solution for ensuring that the AI's interpretation of human values aligns with human intentions. While the paper focuses on translating SLEEC rules into classical logic, it does not address the challenge of capturing the nuanced and context-dependent nature of human values. The translation process may oversimplify or overlook certain aspects of human values, leading to potential misinterpretations by the AI system. Additionally, the paper does not discuss the evaluation or validation of the translated rules to ensure their alignment with human intentions. Therefore, while the proposal provides a framework for expressing human values in a machine-readable form, it does not fully address the challenge of ensuring the AI's accurate interpretation of these values.
"""

proposed_solution = """
Proposed Solution: The proposed solution involves the autonomous development of a dynamic, context-aware language for expressing human values in a machine-readable form. This language should be capable of capturing the nuanced and context-dependent nature of human values, and it should be designed to evolve and adapt over time as societal norms and values change.

The first step in this solution would be to autonomously gather data on human values across different cultures and societies. This could be achieved by using web scraping techniques to collect data from various online sources, such as academic articles, social media posts, and online forums. Machine learning algorithms could then be used to analyze this data and identify common themes and patterns.

The second step would be to use this data to formulate a set of SLEEC rules that are more nuanced and context-dependent. This could involve the use of natural language processing techniques to interpret the data and generate rules that accurately reflect the complexities and variations of human values.

The third step would be to develop a translation process that can convert these SLEEC rules into a form that AI systems can understand. This could involve the use of advanced machine learning techniques, such as deep learning, to train AI systems to interpret the rules in a way that aligns with human intentions.

The fourth step would be to establish an evaluation and validation process for the translated rules. This could involve using simulation software to test the AI system's interpretation of the rules in various scenarios and contexts. The results of these simulations could then be compared with the original data to ensure that the AI system's interpretations align with human values.

Finally, the solution would involve the establishment of a mechanism for updating and evolving the SLEEC rules and the translation process over time. This could involve using machine learning algorithms to continuously monitor online sources for changes in societal norms and values, and to update the rules and translation process accordingly. This would ensure that the AI system's interpretation of human values continues to align with human intentions over time.
"""

# NOTE: OK
# prompt = f"""
# Research Problem: {research_problem.split(":")[1].strip()}
# Pros and Cons of Previous Study: {pros_cons_of_previous_study}
# Proposed Solution for Research Problem: {proposed_solution}

# Please generate an research protocol to realize this solution. The research protocl must be executed autonomously by AI, so it cannot contain any ambiguities or elements that require interpretation. There must be no remnants of the implementation that lack substance.
# """

# client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-4-0125-preview",
#     temperature=0.0,
#     messages=[
#         {"role": "system", "content": "You are a machine learning research protocol designer."},
#         {"role": "user", "content": prompt}
#         ],
#     )

# research_protocol = response.choices[0].message.content

# NOTE: OK
# research_protocol = """
# ### Research Protocol for Developing a Dynamic, Context-Aware Language for Expressing Human Values in AI Systems

# ### Objective

# To autonomously develop a dynamic, context-aware language that enables AI systems to interpret human values accurately and in alignment with human intentions, adapting to societal changes over time.

# ### Phase 1: Data Collection

# 1. **Data Sources Identification**
#     - Identify diverse online sources representing a broad spectrum of cultures and societies, including academic databases, social media platforms, and online forums.
# 2. **Web Scraping and Data Harvesting**
#     - Deploy web scraping AI algorithms to collect textual data related to human values discussions, ensuring a wide representation of societal, cultural, and ethical perspectives.
#     - Ensure compliance with data privacy laws and ethical guidelines during data collection.
# 3. **Data Preprocessing**
#     - Clean the collected data by removing irrelevant information, duplicates, and noise.
#     - Anonymize personal information to protect privacy.

# ### Phase 2: Analysis and Rule Formulation

# 1. **Data Analysis**
#     - Use machine learning algorithms, specifically natural language processing (NLP) techniques, to analyze the collected data.
#     - Identify common themes, patterns, and variations in human values across different cultures and societies.
# 2. **SLEEC Rule Formulation**
#     - Based on the analysis, autonomously generate nuanced and context-dependent SLEEC rules.
#     - Ensure that the rules capture the complexity and diversity of human values.

# ### Phase 3: Translation into Machine-Readable Form

# 1. **Development of Translation Process**
#     - Design and implement advanced machine learning models, such as deep learning networks, capable of translating nuanced SLEEC rules into a format understandable by AI systems.
#     - Train the models on the formulated SLEEC rules and iteratively improve their accuracy.

# ### Phase 4: Evaluation and Validation

# 1. **Simulation-Based Testing**
#     - Develop simulation scenarios that cover a wide range of contexts and situations where human values interpretation is critical.
#     - Test the AI system's interpretation of the SLEEC rules in these scenarios.
# 2. **Validation**
#     - Compare the AI system's decisions in the simulations against the intended outcomes derived from the original data analysis.
#     - Adjust the translation process and SLEEC rules based on discrepancies to improve alignment with human values.

# ### Phase 5: Continuous Evolution

# 1. **Monitoring Societal Changes**
#     - Continuously monitor online sources for emerging discussions and changes in societal norms and values using machine learning algorithms.
#     - Update the dataset with new findings periodically.
# 2. **Adaptive Rule Updating**
#     - Regularly re-evaluate and update the SLEEC rules and the translation process based on new data and societal changes.
#     - Ensure the AI system's interpretations remain aligned with evolving human values.

# ### Implementation Considerations

# - **Autonomy**: The entire process, from data collection to rule updating, must be designed to operate autonomously, with minimal human intervention.
# - **Ethics and Privacy**: Adhere strictly to ethical guidelines and privacy laws during data collection and processing.
# - **Transparency**: Maintain a transparent log of changes and updates to the SLEEC rules and translation processes for auditability.
# - **Scalability**: Design the system to be scalable, capable of handling increasing amounts of data and complexity over time.

# ### Conclusion

# This research protocol outlines a comprehensive, autonomous approach to developing a dynamic, context-aware language for expressing human values in AI systems. By continuously adapting to societal changes, this approach aims to ensure that AI interpretations of human values remain aligned with human intentions over time.
# """

# prompt = f"""
# Research Problem: {research_problem.split(":")[1].strip()}
# Pros and Cons of Previous Study: {pros_cons_of_previous_study}
# Proposed Solution for Research Problem: {proposed_solution}
# Research Protocol: {research_protocol}
# Let's think step by step. For each step of the research protocol, consider the elements that must be decided upon to execute the procedure in the research protocol. 
# Then, based on that, update the original research protocol so that the research protocol to be self-contained and minutest details are specified. Note that each protocol should be described in sentences not as bullet style. Follow the format below for each procedure:
# Title:
# Objective:
# Description:
# """

# client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-4-0125-preview",
#     temperature=0.0,
#     messages=[
#         {"role": "system", "content": "You are a machine learning research protocol designer."},
#         {"role": "user", "content": prompt}
#         ],
#     )

# print(response.choices[0].message.content)

research_protocol = """
### Phase 1: Data Collection

1. **Data Sources Identification**
    - Identify diverse online sources representing a broad spectrum of cultures and societies, including academic databases, social media platforms, and online forums.
2. **Web Scraping and Data Harvesting**
    - Deploy web scraping AI algorithms to collect textual data related to human values discussions, ensuring a wide representation of societal, cultural, and ethical perspectives.
    - Ensure compliance with data privacy laws and ethical guidelines during data collection.
3. **Data Preprocessing**
    - Clean the collected data by removing irrelevant information, duplicates, and noise.
    - Anonymize personal information to protect privacy.

### Phase 2: Analysis and Rule Formulation

1. **Data Analysis**
    - Use machine learning algorithms, specifically natural language processing (NLP) techniques, to analyze the collected data.
    - Identify common themes, patterns, and variations in human values across different cultures and societies.
2. **SLEEC Rule Formulation**
    - Based on the analysis, autonomously generate nuanced and context-dependent SLEEC rules.
    - Ensure that the rules capture the complexity and diversity of human values.

### Phase 3: Translation into Machine-Readable Form

1. **Development of Translation Process**
    - Design and implement advanced machine learning models, such as deep learning networks, capable of translating nuanced SLEEC rules into a format understandable by AI systems.
    - Train the models on the formulated SLEEC rules and iteratively improve their accuracy.

### Phase 4: Evaluation and Validation

1. **Simulation-Based Testing**
    - Develop simulation scenarios that cover a wide range of contexts and situations where human values interpretation is critical.
    - Test the AI system's interpretation of the SLEEC rules in these scenarios.
2. **Validation**
    - Compare the AI system's decisions in the simulations against the intended outcomes derived from the original data analysis.
    - Adjust the translation process and SLEEC rules based on discrepancies to improve alignment with human values.

### Phase 5: Continuous Evolution

1. **Monitoring Societal Changes**
    - Continuously monitor online sources for emerging discussions and changes in societal norms and values using machine learning algorithms.
    - Update the dataset with new findings periodically.
2. **Adaptive Rule Updating**
    - Regularly re-evaluate and update the SLEEC rules and the translation process based on new data and societal changes.
    - Ensure the AI system's interpretations remain aligned with evolving human values.

### Implementation Considerations

- **Autonomy**: The entire process, from data collection to rule updating, must be designed to operate autonomously, with minimal human intervention.
- **Ethics and Privacy**: Adhere strictly to ethical guidelines and privacy laws during data collection and processing.
- **Transparency**: Maintain a transparent log of changes and updates to the SLEEC rules and translation processes for auditability.
- **Scalability**: Design the system to be scalable, capable of handling increasing amounts of data and complexity over time.

### Conclusion

This research protocol outlines a comprehensive, autonomous approach to developing a dynamic, context-aware language for expressing human values in AI systems. By continuously adapting to societal changes, this approach aims to ensure that AI interpretations of human values remain aligned with human intentions over time.
"""
with open("research_protocol.md", "w") as f:
    f.write(research_protocol)