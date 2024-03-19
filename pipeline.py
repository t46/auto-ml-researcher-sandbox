from openai import OpenAI
from research_problem_generation.research_problem_generation import generate_research_problem
from method_proposition.proposed_method_generation import generate_proposed_method
from method_proposition.proposed_method_code_generation import generate_proposed_method_code
from experiment.experiment_design_generation import generate_experiment_design
from experiment.model_data_selection import select_data, select_models
from experiment.experiment_code_generation import generate_experiment_code

client = OpenAI()
high_level_problem = "AI alignment problem: the problem refers to the challenge that artificial intelligence (AI) systems are designed to act in ways that are beneficial to humans and aligned with human values and interests."
research_problem = generate_research_problem(high_level_problem, client)
proposed_method = generate_proposed_method(research_problem, client)
_ = generate_proposed_method_code(proposed_method, client)
experiment_design = generate_experiment_design(research_problem, proposed_method, client)
dataset_names = select_data(research_problem, proposed_method, experiment_design)
model_names = select_models(research_problem, proposed_method, experiment_design)
_ = generate_experiment_code(research_problem, proposed_method, dataset_names, dataset_names, client)