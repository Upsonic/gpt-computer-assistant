from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel

from openai import AsyncAzureOpenAI

from pydantic import BaseModel
from pydantic_ai.result import ResultData
from fastapi import HTTPException, status

from ...storage.configuration import Configuration


from ...tools_server.function_client import FunctionToolManager






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
            if not azure_endpoint or not azure_api_version or not azure_api_key:
                return {"status_code": 401, "detail": "No API key provided. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, and AZURE_OPENAI_API_KEY in your configuration."}
            model = AsyncAzureOpenAI(api_version=azure_api_version, azure_endpoint=azure_endpoint, api_key=azure_api_key)
            model = OpenAIModel('gpt-4o', openai_client=model)

        else:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported LLM model: {llm_model}"
            )

        roulette_agent = Agent(
            model,
            result_type=response_format,
        )



        with FunctionToolManager() as function_client:
            for each in function_client.get_tools_by_name(tools):
                roulette_agent.tool_plain(each, retries=5)

        result = roulette_agent.run_sync(prompt)

        return result.data


Call = CallManager()
