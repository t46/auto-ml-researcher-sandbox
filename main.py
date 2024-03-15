from researchagent.agent import Agent
from researchagent.tools import tools

task = "Say Hello"
background_info = {
    "research_problem": "Hello",
    "proposed_solution": "Hello",
    "previous_study": "Hello",
}
agent = Agent(tools, task)
agent.run()