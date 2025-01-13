import copy
import time
import cloudpickle
import dill
import base64
import httpx
from typing import Any, List, Dict, Optional, Type, Union
from pydantic import BaseModel

from ..tasks.tasks import Task

from ..printing import call_end

class NoAPIKeyException(Exception):
    pass


class UnsupportedLLMModelException(Exception):
    pass


class CallErrorException(Exception):
    pass

from ..tasks.task_response import ObjectResponse

from ..agent_configuration.agent_configuration import AgentConfiguration

class Agent:


    def agent_(self, agent_configuration: AgentConfiguration):
        print(agent_configuration)


        tools = ["google", "read_website"]

        class SearchResult(ObjectResponse):
            any_customers: bool
            products: List[str]
            services: List[str]
            potential_competitors: List[str]

        task_1 = Task(description=f"Make a search for {agent_configuration.company_url}", tools=tools, response_format=SearchResult)

        self.call(task_1, llm_model="gpt-4o-azure")

        print(task_1.response)

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
        for each in sub_tasker.response.sub_tasks:
            sub_tasks.append(Task(description=each.description))

        for each in sub_tasks:
            each.tools = task.tools

            each.context = sub_tasks

        sub_tasks[-1].response_format = task.response_format


        return sub_tasks



