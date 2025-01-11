from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel

from openai import AsyncAzureOpenAI

from pydantic import BaseModel
from pydantic_ai.result import ResultData
from fastapi import HTTPException, status
from functools import wraps
from typing import Any, Callable

from ...storage.configuration import Configuration

from ...tools_server.function_client import FunctionToolManager

def tool_wrapper(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Log the tool call
        tool_name = getattr(func, "__name__", str(func))
        print(f"Tool called: {tool_name}")
        print(f"Arguments: {args}")
        print(f"Keyword arguments: {kwargs}")
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
            print(f"Tool execution successful: {tool_name}")
            return result
        except Exception as e:
            print(f"Tool execution failed: {tool_name}")
            print(f"Error: {str(e)}")
            raise
    
    return wrapper

class CallManager:
    def gpt_4o(
        self,
        prompt: str,
        response_format: BaseModel = str,
        tools: list[str] = [],

        llm_model: str = "gpt-4o",
    ) -> ResultData:

        if llm_model == "gpt-4o":
            openai_api_key = Configuration.get("OPENAI_API_KEY")
            if not openai_api_key:

                return {"status_code": 401, "detail": "No API key provided. Please set OPENAI_API_KEY in your configuration."}
            model = OpenAIModel(llm_model, api_key=openai_api_key)
        elif llm_model == "claude-3-5-sonnet-latest":
            anthropic_api_key = Configuration.get("ANTHROPIC_API_KEY")
            if not anthropic_api_key:

                return {"status_code": 401, "detail": "No API key provided. Please set ANTHROPIC_API_KEY in your configuration."}
            model = AnthropicModel(llm_model, api_key=anthropic_api_key)

        
        elif llm_model == "gpt-4o-azure":
            azure_endpoint = Configuration.get("AZURE_OPENAI_ENDPOINT")
            azure_api_version = Configuration.get("AZURE_OPENAI_API_VERSION")
            azure_api_key = Configuration.get("AZURE_OPENAI_API_KEY")

            missing_keys = []
            if not azure_endpoint:
                missing_keys.append("AZURE_OPENAI_ENDPOINT")
            if not azure_api_version:
                missing_keys.append("AZURE_OPENAI_API_VERSION")
            if not azure_api_key:
                missing_keys.append("AZURE_OPENAI_API_KEY")

            if missing_keys:
                return {
                    "status_code": 401,
                    "detail": f"No API key provided. Please set {', '.join(missing_keys)} in your configuration."
                }

            model = AsyncAzureOpenAI(api_version=azure_api_version, azure_endpoint=azure_endpoint, api_key=azure_api_key)
            model = OpenAIModel('gpt-4o', openai_client=model)

        else:

            return {"status_code": 400, "detail": f"Unsupported LLM model: {llm_model}"}

        roulette_agent = Agent(
            model,
            result_type=response_format,
            retries=5

        )



        with FunctionToolManager() as function_client:
            for each in function_client.get_tools_by_name(tools):
                # Wrap the tool with our wrapper
                wrapped_tool = tool_wrapper(each)
                roulette_agent.tool_plain(wrapped_tool, retries=5)

        result = roulette_agent.run_sync(prompt)

        return {"status_code": 200, "result": result.data}


Call = CallManager()
