from dataset_retrieval import DescriptionDatasetRetriever

instruction = """
classify news articles
"""

retriever = DescriptionDatasetRetriever()
dataset = retriever.retrieve_dataset_dict(instruction=instruction)

print(dataset)