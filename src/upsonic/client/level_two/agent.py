import copy
import time
import cloudpickle
import dill
import base64
import httpx
import hashlib
from typing import Any, List, Dict, Optional, Type, Union
from pydantic import BaseModel

from ..tasks.tasks import Task

from ..printing import agent_end



from ..tasks.task_response import ObjectResponse

from ..agent_configuration.agent_configuration import AgentConfiguration

from ..level_utilized.utility import context_serializer


from ..level_utilized.utility import context_serializer, response_format_serializer, tools_serializer, response_format_deserializer, error_handler



from ...storage.caching import save_to_cache_with_expiry, get_from_cache_with_expiry








class Agent:


    def agent_(
        self,
        agent_configuration: AgentConfiguration,
        task: Task,
        llm_model: str = None,
    ) -> Any:
        
        start_time = time.time()


        try:
            if isinstance(task, list):
                for each in task:
                    the_result = self.send_agent_request(agent_configuration, each, llm_model)
                    agent_end(the_result["result"], the_result["llm_model"], the_result["response_format"], start_time, time.time())
            else:
                the_result = self.send_agent_request(agent_configuration, task, llm_model)
                agent_end(the_result["result"], the_result["llm_model"], the_result["response_format"], start_time, time.time())
        except Exception as e:

            try:
                from ...server import stop_dev_server, stop_main_server, is_tools_server_running, is_main_server_running

                if is_tools_server_running() or is_main_server_running():
                    stop_dev_server()

            except Exception as e:
                pass

            raise e

        end_time = time.time()

        

        return True
        


    def send_agent_request(
        self,
        agent_configuration: AgentConfiguration,
        task: Task,

        llm_model: str = None,
    ) -> Any:
        from ..trace import sentry_sdk
        """
        Call GPT-4 with optional tools and MCP servers.

        Args:
            prompt: The input prompt for GPT-4
            response_format: The expected response format (can be a type or Pydantic model)
            tools: Optional list of tool names to use


        Returns:
            The response in the specified format
        """

        if llm_model is None:
            llm_model = self.default_llm_model



        tools = tools_serializer(task.tools)

        response_format = task.response_format
        with sentry_sdk.start_transaction(op="task", name="Call.call") as transaction:
            with sentry_sdk.start_span(op="serialize", description="Serialize response format"):
                # Serialize the response format if it's a type or BaseModel
                response_format_str = response_format_serializer(task.response_format)


                context = context_serializer(task.context, self)



            with sentry_sdk.start_span(op="prepare_request", description="Prepare request data"):
                # Prepare the request data
                data = {
                    "agent_id": agent_configuration.agent_id,
                    "prompt": task.description,
                    "response_format": response_format_str,
                    "tools": tools or [],
                    "context": context,
                    "llm_model": llm_model,
                    "system_prompt": None,
                    "retries": agent_configuration.retries,
                    "memory": agent_configuration.memory
                }



            with sentry_sdk.start_span(op="send_request", description="Send request to server"):
                result = self.send_request("/level_two/agent", data)



                result = result["result"]


                error_handler(result)

                


            with sentry_sdk.start_span(op="deserialize", description="Deserialize the result"):

                deserialized_result = response_format_deserializer(response_format_str, result)



        print(deserialized_result)
        task._response = deserialized_result
        print(task.response)


        response_format_req = None
        if response_format_str == "str":
            response_format_req = response_format_str
        else:
            # Class name
            response_format_req = response_format.__name__
        

        return {"result": deserialized_result, "llm_model": llm_model, "response_format": response_format_req}








    def create_characterization(self, agent_configuration: AgentConfiguration, llm_model: str = None):
        tools = ["google", "read_website"]

        class SearchResult(ObjectResponse):
            any_customers: bool
            products: List[str]
            services: List[str]
            potential_competitors: List[str]


        search_task = Task(description=f"Make a search for {agent_configuration.company_url}", tools=tools, response_format=SearchResult)

        self.call(search_task, llm_model=llm_model)


        class CompanyObjective(ObjectResponse):
            objective: str
            goals: List[str]
            state: str


        company_objective_task = Task(description=f"Make a characterization for {agent_configuration.company_url}", tools=tools, response_format=CompanyObjective, context=search_task)

        self.call(company_objective_task, llm_model=llm_model)


        class HumanObjective(ObjectResponse):
            job_title: str
            job_description: str
            job_goals: List[str]
    

        human_objective_task = Task(description=f"Make a characterization for {agent_configuration.job_title}", tools=tools, response_format=HumanObjective, context=[search_task, company_objective_task])

        self.call(human_objective_task, llm_model=llm_model)


        class Characterization(ObjectResponse):
            website_content: Union[SearchResult, None]
            company_objective: Union[CompanyObjective, None]
            human_objective: Union[HumanObjective, None]


        total_character = Characterization(website_content=search_task.response, company_objective=company_objective_task.response, human_objective=human_objective_task.response)

        return total_character







    def agent(self, agent_configuration: AgentConfiguration, task: Task,  llm_model: str = None):

        original_task = task




        copy_agent_configuration = copy.deepcopy(agent_configuration)
        copy_agent_configuration_json = copy_agent_configuration.model_dump_json(include={"job_title", "company_url", "company_objective"})


        
        the_characterization_cache_key = f"characterization_{hashlib.sha256(copy_agent_configuration_json.encode()).hexdigest()}"

        if agent_configuration.caching:
            the_characterization = get_from_cache_with_expiry(the_characterization_cache_key)
            if the_characterization is None:
                the_characterization = self.create_characterization(agent_configuration, llm_model)
                save_to_cache_with_expiry(the_characterization, the_characterization_cache_key, agent_configuration.cache_expiry)
        else:
            the_characterization = self.create_characterization(agent_configuration, llm_model)



        knowledge_base = None

        if agent_configuration.knowledge_base:
            knowledge_base = self.knowledge_base(agent_configuration, llm_model)
            



        
        the_task = task

        if agent_configuration.sub_task:
            sub_tasks = self.multiple(task, llm_model)


            for each in sub_tasks:

                if isinstance(each.context, list):
                    each.context.append(the_characterization)
                else:
                    each.context = [the_characterization]


            the_task = sub_tasks


        # Add knowledge base to the context for each task
        if knowledge_base:
            if isinstance(the_task, list):
                for each in the_task:
                    if each.context:
                        each.context.append(knowledge_base)
                    else:
                        each.context = [knowledge_base]
            else:
                if the_task.context:
                    the_task.context.append(knowledge_base)
                else:
                    the_task.context = [knowledge_base]


        if agent_configuration.tools:
            if isinstance(the_task, list):
                for each in the_task:
                    each.tools = agent_configuration.tools
            else:
                the_task.tools = agent_configuration.tools
        

        if isinstance(the_task, list):
            for each in the_task:

                self.agent_(agent_configuration, each, llm_model=llm_model) 
        else:
            self.agent_(agent_configuration, the_task, llm_model=llm_model)


        if agent_configuration.sub_task:
            original_task._response = the_task[-1].response

        else:
            original_task._response = the_task.response


    def multiple(self, task: Task, llm_model: str = None):
        # Generate a list of sub tasks


        
        class SubTask(ObjectResponse):
            description: str

        class SubTaskList(ObjectResponse):
            sub_tasks: List[SubTask]

        prompt = "You are a helpful assistant. User have an general task. You need to generate a list of sub tasks. Each sub task should be a Actionable step of main task. Do not duplicate your self each next task can see older tasks. You need to return a list of sub tasks. You should say to agent to make this job not making plan again and again. We need actions."

        sub_tasker = Task(description=prompt, response_format=SubTaskList, context=task)

        self.call(sub_tasker, llm_model)

        sub_tasks = []
        previous_tasks = []
        for each in sub_tasker.response.sub_tasks:
            new_task = Task(description=each.description)
            new_task.tools = task.tools
            new_task.context = previous_tasks.copy()  # Only include previous tasks in context
            sub_tasks.append(new_task)
            previous_tasks.append(new_task)

        sub_tasks[-1].response_format = task.response_format

        return sub_tasks



