import cloudpickle
import dill
import base64
import httpx
from typing import Any, List, Dict, Optional, Type, Union
from pydantic import BaseModel

from ..tasks.tasks import Task

class NoAPIKeyException(Exception):
    pass


class UnsupportedLLMModelException(Exception):
    pass


class CallErrorException(Exception):
    pass


class Call:


    def call(
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

        tools = task.tools


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



            with sentry_sdk.start_span(op="prepare_request", description="Prepare request data"):
                # Prepare the request data
                data = {
                    "prompt": task.description,
                    "response_format": response_format_str,
                    "tools": tools or [],

                    "llm_model": llm_model,
                }



            with sentry_sdk.start_span(op="send_request", description="Send request to server"):
                # Use the send_request method from the Base class
                result = self.send_request("/level_one/gpt4o", data)
            
                
                if result["status_code"] == 401:
                    raise NoAPIKeyException(result["result"]["detail"])
                
                if result["status_code"] == 400:
                    raise UnsupportedLLMModelException(result["result"]["detail"])

                if result["status_code"] == 500:
                    raise CallErrorException(result["result"])

            with sentry_sdk.start_span(op="deserialize", description="Deserialize the result"):
                # Deserialize the result
                if response_format_str != "str":
                    decoded_result = base64.b64decode(result["result"])
                    deserialized_result = cloudpickle.loads(decoded_result)
                else:
                    deserialized_result = result["result"]



        task._response = deserialized_result

        return True
