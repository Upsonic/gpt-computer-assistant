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


class Call:


    def call(
        self,
        task: Union[Task, List[Task]],
        llm_model: str = None,
    ) -> Any:
        
        start_time = time.time()


        try:
            if isinstance(task, list):
                for each in task:
                    the_result = self.call_(each, llm_model)
            else:
                the_result = self.call_(task, llm_model)
        except Exception as e:

            try:
                from ...server import stop_dev_server, stop_main_server, is_tools_server_running, is_main_server_running

                if is_tools_server_running() or is_main_server_running():
                    stop_dev_server()

            except Exception as e:
                pass

            raise e

        end_time = time.time()

        call_end(the_result["result"], the_result["llm_model"], the_result["response_format"], start_time, end_time)

        return True

    def call_(
        self,
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

        tools_ = task.tools

        tools = []
        for i in tools_:


            if isinstance(i, type):

                tools.append(i.__name__+".*")
            # If its a string, get the name of the string
            elif isinstance(i, str):

                tools.append(i)

        response_format = task.response_format
        with sentry_sdk.start_transaction(op="task", name="Call.call") as transaction:
            with sentry_sdk.start_span(op="serialize", description="Serialize response format"):
                # Serialize the response format if it's a type or BaseModel
                if response_format is None:
                    response_format_str = "str"
                elif isinstance(response_format, (type, BaseModel)):
                    # If it's a Pydantic model or other type, cloudpickle and base64 encode it
                    the_module = dill.detect.getmodule(response_format)
                    if the_module is not None:
                        cloudpickle.register_pickle_by_value(the_module)
                    pickled_format = cloudpickle.dumps(response_format)
                    response_format_str = base64.b64encode(pickled_format).decode("utf-8")
                else:
                    response_format_str = "str"


                context = task.context
                if context is not None:
                    copy_of_context = copy.deepcopy(context)
                    if isinstance(copy_of_context, list):
                        for each in copy_of_context:

                            each.tools = []
                            each.response_format = None


                            the_module = dill.detect.getmodule(each)
                            if the_module is not None:
                                cloudpickle.register_pickle_by_value(the_module)
                            pickled_context = cloudpickle.dumps(each)
                            each = base64.b64encode(pickled_context).decode("utf-8")
                    else:
                        # Serialize the context
                        copy_of_context.tools = []
                        copy_of_context.response_format = None
                        the_module = dill.detect.getmodule(copy_of_context)
                        if the_module is not None:
                            cloudpickle.register_pickle_by_value(the_module)
                    pickled_context = cloudpickle.dumps(copy_of_context)
                    context = base64.b64encode(pickled_context).decode("utf-8")
                else:
                    context = None



            with sentry_sdk.start_span(op="prepare_request", description="Prepare request data"):
                # Prepare the request data
                data = {
                    "prompt": task.description,
                    "response_format": response_format_str,
                    "tools": tools or [],
                    "context": context,
                    "llm_model": llm_model,
                }



            with sentry_sdk.start_span(op="send_request", description="Send request to server"):
                result = self.send_request("/level_one/gpt4o", data)



                result = result["result"]


                
                if result["status_code"] == 401:
                    raise NoAPIKeyException(result["detail"])
                
                if result["status_code"] == 400:
                    raise UnsupportedLLMModelException(result["detail"])

                if result["status_code"] == 500:
                    raise CallErrorException(result)
                


            with sentry_sdk.start_span(op="deserialize", description="Deserialize the result"):
                # Deserialize the result
                if response_format_str != "str":
                    decoded_result = base64.b64decode(result["result"])
                    deserialized_result = cloudpickle.loads(decoded_result)
                else:
                    deserialized_result = result["result"]



        task._response = deserialized_result


        response_format_req = None
        if response_format_str == "str":
            response_format_req = response_format_str
        else:
            # Class name
            response_format_req = response_format.__name__
        

        return {"result": deserialized_result, "llm_model": llm_model, "response_format": response_format_req}

