from openai import OpenAI
import re
import ast
import sys
import os
import anthropic

################ Prompt ################
prompt_template = """You are a machine learning researcher. 
                    
                    You have access to the following tools:
                    {tools_prompt}

                    Accomplish this task:
                    Task:
                    {task_description}

                    Initial Plan: 
                    {plan}

                    Follow these instructions and do not forget them:
                    - First, modify the Initial Plan so that it can be completed with available tools and record it in the Plan and Status. You can integrate different tasks or further divide them into more detailed parts. If the necessary tools are not available, include in your plan the creation and execution of the tools needed. You can revise the plan later.
                    - Plan and Status should well organized and succinctly keep track of 1) detailed plan (can be revised), 2) what steps have been done and what steps are in progress, 3) short results and conclusions of each step after it has been performed. 
                    - Plan and Status must only include progress that has been made by previous steps. It should not include results not directly confirmed by the previous observation. 
                    - Follow the plan and try to achieve the task as straightforwardly as possible.
                    - If you think the task cannot be performed, consider how you can accomplish it using the tools you have been given. You can do anything with tools. Never give up.
                    - Do not just finish outputting plan, create and execute the task.
                    - If you believe you have solved the problem, you can use the Final Answer action to submit your answer. You can only submit once, so double check that you have achieved the task before submitting.

                    Always respond in this format exactly:
                    {routine_prompt}
                    Observation: 
                    ```
                    the result of the action
                    ```

                    """

routine_prompt_dict = {
    "Reflection": "What does the observation mean? If there is an error, what caused the error and how to debug?",
    "Plan and Status": "The full plan, with current status and confirmed results of each step briefly annotated. It must only include progress that has been made by previous steps. If there is any update, enclose the new update text in double asterisks **like this**. If there is no update, just copy the previous step Plan and Status. The high level plan from the previous step should be fully retained, unless it is intentionally revised.",
    "Fact Check": "List all objective statements in the updates to Plan and Status one by one and point out whether it is guessed versus directly confirmed by the previous observation directly above. Performance numbers can only be confirmed by running the code and observing the output.",
    "Thought": "What you are currently doing, what actions to perform and why",
    "Action": "the action to take, should be one of the names of the tools",
    "Action Input": "the input to the action as a valid JSON string",
}

class Agent:
    def __init__(self, tools, task, plan):
        self.tools = tools
        self.tool_names = [tool.name for tool in tools] + ["Final Answer"]
        self.task = task
        self.initial_prompt = prompt_template.format(
            tools_prompt=self.construct_tools_prompt(tools),
            task_description=self.task,
            plan=plan,
            routine_prompt="\n".join([f"{k}: {v}" for k, v in routine_prompt_dict.items()])
            )
        self.client = OpenAI()
        self.routine_prompt_dict = routine_prompt_dict
        self.history_steps = []
        self.max_steps_in_context = 5
        self.max_observation_steps_in_context = 3
        self.max_retries = 2
        self.max_step_total = 10
        self.log_dir = os.path.join(".", "agent_log")
        
        # self.log_dir を作成。self.log_dir がすでに存在する場合は一度削除して新しく作成
        if os.path.exists(self.log_dir):
            import shutil
            shutil.rmtree(self.log_dir)
        os.makedirs(self.log_dir)

        # research_log.log を作成
        with open("./research_log.log", "w") as f:
            f.write("")
        # main_log を作成
        with open(os.path.join(self.log_dir , "main_log"), "w") as f:
            f.write("")
        # agent_log を作成
        with open(os.path.join(self.log_dir , "agent_log"), "w") as f:
            f.write("")

    
    def run(self):
        last_steps = self.max_steps_in_context
        last_observation_step = self.max_observation_steps_in_context

        with open(os.path.join(self.log_dir , "main_log"), "a", 1) as f:
            f.write(self.initial_prompt + "\n")

        for step in range(self.max_step_total):
            
            ################ Add Summary of Relevant History ################
            prompt = self.initial_prompt
            current_step = len(self.history_steps)
            if current_step > self.max_steps_in_context:
                relevant_history = self.retrieve_relevant_history(current_plan="")  # TODO: add current plan
                prompt += f"""
                            Here is a summary of relevant actions and observations you have done:
                            ```
                            {relevant_history}
                            ```
                            Here are the exact several steps you have done most recently (up to 3 steps):
                            """
            else:
                prompt += "\nNow let's start!\n\n"
            
            ################ Add Recent History ################
            for past_step in range(max(current_step - last_steps, 0), current_step):
                action_string = ""
                action_string = self.print_action(self.history_steps[past_step]["action"], self.routine_prompt_dict)

                prompt += anthropic.AI_PROMPT + "\n"+ action_string + "\nObservation:"
                if current_step - past_step > last_observation_step:
                    prompt += "<Done>\n\n"
                else:
                    prompt += "\n```\n" + self.history_steps[past_step]["observation"] + "\n```\n\n"

            ################ Call LLM Until the Response is Valid ################
            valid_response = False
            for _ in range(self.max_retries):
                log_file = os.path.join(self.log_dir , f"step_{current_step}_log.log")
                llm_response = self.get_llm_response(prompt=prompt, model="gpt-4-0125-preview", log_file=log_file)
                print(llm_response)
                
                try:
                    parsed_llm_response = self.parse_llm_response(llm_response, routine_prompt_dict)
                    assert parsed_llm_response["Action"] in self.tool_names
                    valid_response = True
                    break
                except:
                    print("Step", current_step, file=sys.stderr)
                    print(anthropic.AI_PROMPT + "\n" + llm_response + "\nObservation:\n", file=sys.stderr)
                    print("Response is invalid and discarded", file=sys.stderr)
                    prompt += "\n\n Your response was in incorrect format. Please provide a valid response with all entries: " + ", ".join(self.routine_prompt_dict) + "\n\n"

            # with open(os.path.join(self.log_dir , "main_log"), "a", 1) as f:
            #     f.write("\n```\n" + response.choices[0].message.content + "\n```\n\n")

            with open(os.path.join(self.log_dir , "main_log"), "a", 1) as f:
                f.write("Step " + str(current_step) + ":\n")
                f.write(anthropic.AI_PROMPT + "\n" + self.print_action(parsed_llm_response, routine_prompt_dict) + "\nObservation:\n")


            ################ Execute Action ################
            if not valid_response:
                return "No valid response after max_retries"

            action = parsed_llm_response["Action"]
            if action == "Final Answer":
                print("Final Answer")
                break
            parsed_llm_response["Plan and Status"] = self.postprocess_plan_and_status(parsed_llm_response["Plan and Status"])

            observation = self.execute_action(action, self.parse_action_input(parsed_llm_response["Action Input"]))

            # if observation is too long, we need to summarize it
            if len(observation) > 10000:  # 5000
                log_file = os.path.join(self.log_dir , f"step_{current_step}_summarize_observation_log.log")

                print("Observation is too long. Summarizing...", file=sys.stderr)
                observation = self.summarize_observation(self.print_action(parsed_llm_response, self.routine_prompt_dict), observation, log_file)

            print('Observation: ' + observation)

            ################ Update History ################
            self.history_steps.append({"step_idx": step, "action": parsed_llm_response, "observation": observation})

            with open(os.path.join(self.log_dir , "main_log"), "a", 1) as f:
                f.write("\n```\n" + self.history_steps[-1]["observation"] + "\n```\n\n")

            ################ Write Research Log for Retrieval ################
            summary_of_last_step = "Too long to summarize."
            for _ in range(self.max_retries):
                try:
                    log_file = os.path.join(self.log_dir , f"step_{current_step}_summary_log.log")
                    summary_of_last_step = self.summarize_action_and_observation(self.print_action(self.history_steps[-1]["action"], self.routine_prompt_dict), self.history_steps[-1]["observation"], log_file = log_file)
                    break
                except Exception as e:
                    print(e)
                    print("Trying again.")

            with open("./research_log.log", "a") as f:
                f.write("\n\nStep " + str(current_step) + ":\n" + summary_of_last_step + "\n")

        # TODO: save the agent
        # step_idx = len(env.trace.steps) - 1
        # self.save(os.path.join(self.log_dir , f"agent_{step_idx}_{curr_step}.json"))
    


    ############################### Utility Methods ###############################

    ################ Construct Prompt ################
    def construct_tool_prompt(self, tool):
        """ Construct the prompt for a single tool."""
        tool_input = ",\n            ".join([f"\"{k}\": [{v}]" for k, v in tool.tool_input.items()])

        tools_prompt = f"""{tool.description}
        Usage:
        ```
        Action: {tool.name}
        Action Input: {{
            {tool_input}
        }}
        Observation: [{tool.return_value}]
        ```
            """.strip() + "\n\n"
        return tools_prompt

    def construct_tools_prompt(self, tools):
        """ Construct the prompt for all tools."""
        tools_prompt = ""
        for tool in tools:
            tools_prompt += f"""- {tool.name}:
        """
            tools_prompt += self.construct_tool_prompt(tool)
        return tools_prompt
    
    ################ Get LLM Response ################
    def get_llm_response(self, prompt, model, log_file=None):
        """ Get the response from LLM given the prompt."""
        response = self.client.chat.completions.create(
                        model=model,
                        temperature=0.0,
                        messages=[{"role": "user", "content": prompt}],
                        )
        if log_file is not None:
            with open(log_file, "a") as f:
                f.write("\n===================prompt=====================\n")
                f.write(f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}")
                f.write(f"\n===================response=====================\n")
                f.write(response.choices[0].message.content)
                f.write("\n\n")
        return response.choices[0].message.content
    
    ################ Parse and Postprocess LLM Output ################
    def parse_llm_response(self, llm_response, routine_prompt_dict):
        """ Parse the component of the task execution routine from the string generated by LLM using regex."""
        pattern = ""
        for routine_component in routine_prompt_dict:
            pattern += f"{routine_component}:([\s\S]*)"  # TODO: pattern 全部まとめてるけど、例えば Action はあるけど Reflection がない時とか大丈夫なんだろうか。 
        matched_llm_output = re.search(pattern, llm_response, re.MULTILINE)
        if matched_llm_output is None:
            raise Exception("Invalid: " + llm_response)

        parsed_llm_response = {routine_component: matched_output.strip() for routine_component, matched_output in zip(routine_prompt_dict, matched_llm_output.groups())}
        return parsed_llm_response

    def parse_action_input(self, action_input_response):
        dict_pattern = r'\{.*?\}'
        
        match = re.search(dict_pattern, action_input_response, re.DOTALL)
        if match:
            action_input_str = match.group(0)
            try:
                action_input_dict = ast.literal_eval(action_input_str)
                return action_input_dict
            except ValueError:
                raise Exception("Invalid: " + action_input_response)
        else:
            raise Exception("Invalid: " + action_input_response)

    def postprocess_plan_and_status(self, plan_and_status):
        new_plan_and_status = plan_and_status.strip("```") + "\n\n" 
        return new_plan_and_status.replace("**", "")
        

    ################ Execute Action ################
    def execute_action(self, action, action_input):
        """ Execute the action with the given input."""
        for tool in self.tools:
            if tool.name == action:
                return str(tool.function(**action_input))
            
    ################ Retrieve History ################
    def retrieve_relevant_history(self, current_plan, work_dir = "."):

        research_log_content = open(os.path.join(work_dir, "research_log.log")).read()
        prompt = f"""We are trying to solve this task: 
                    {self.task}

                    Your current Plan and Status:
                    {current_plan}
                        
                    Your current research log:
                    ```
                    {research_log_content}
                    ```

                    Concisely summarize and list all relevant information from the research log that will be helpful for future step in this format:
                    """
        llm_response = self.get_llm_response(prompt=prompt, model="gpt-3.5-turbo-0125")

        return llm_response
            
    ################ Update History ################
    def print_action(self, entries, routine_prompt_dict):
        """ Print the action in a readable format."""
        return "".join([ k + ": " + entries[k] for k in  routine_prompt_dict])
    
    def summarize_observation(self, action, observation, log_file, block_size = 10000):
        """ Summarize the observation if it is too long with a sliding window of size bs """

        blocks = [observation[i: i + block_size] for i in range(0, len(observation), block_size)]
        descriptions = []
        for idx, block in enumerate(blocks):
            start_line_number = block_size * idx + 1
            end_line_number = block_size * idx + 1 + len(block)
            prompt = f"""
                        {action}

                        The full observation is too long. Given this (partial) observation from character {start_line_number} to character {end_line_number}: 
                        ``` 
                        {block}
                        ```
                        Summarize the observation concisely in this format:
                        [Observation]: Summarize all relevant details in the observation objectively

                        Do not include any result that is guessed rather than directly confirmed by the observation. Do not include additional information or suggestions.
                    """
            llm_response = self.get_llm_response(prompt=prompt, model="gpt-3.5-turbo-0125", log_file=log_file + f"_{idx}")
            descriptions.append(llm_response)
        if len(descriptions) != 1:
            descriptions = "\n\n".join(["Segment {idx}: \n\n" + s for s in descriptions])
            prompt = f"""
                        {action}

                        The full observation is too long. 
                        Given summaries for each segments of the whole observation, summarize to get a cohesive description of the entire observation.
                        {descriptions}

                        Summarize the observation concisely in this format:
                        [Observation]: Summarize all relevant details in the observation objectively

                        Do not include any result that is guessed rather than directly confirmed by the observation. Do not include additional information or suggestions.
                        """
            llm_response = self.get_llm_response(prompt=prompt, model="gpt-3.5-turbo-0125", log_file=log_file)

        try:
            return llm_response.split("[Observation]:")[1]
        except:
            return llm_response
        
    def summarize_action_and_observation(self, action, observation, **kwargs):
        """ Summarize the action and observation to an entry in the research log """

        prompt = f"""Given your action and the observation: 
        {action} 
        [Observation]:
        ```
        {observation}
        ```
        Summarize your action and the observation in this format:
        [Reasoning]: Summarize the reasoning behind the action
        [Action]: Summarize all relevant details of the action objectively
        [Observation]: Summarize all relevant details in the observation objectively
        Do not include any result that is guessed rather than directly confirmed by the observation. Do not include additional information or suggestions.
        """

        summary = "[Reasoning]:" + self.get_llm_response(prompt=prompt, model="gpt-3.5-turbo-0125", log_file=kwargs["log_file"]).split("[Reasoning]:")[1]
        return summary