from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel

from pydantic import BaseModel
from pydantic_ai.result import ResultData
from fastapi import HTTPException, status

from ...storage.configuration import Configuration

from ...tools_server.mcp_client import MCPToolManager
from ...tools_server.function_client import FunctionToolManager






class CallManager:
    def gpt_4o(
        self,
        prompt: str,
        response_format: BaseModel = str,
        tools: list[str] = [],
        mcp_servers: list[dict[str, str]] = [],
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
        else:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported LLM model: {llm_model}"
            )

        roulette_agent = Agent(
            model,
            result_type=response_format,
        )

        all_mcp_tools = []
        for each in mcp_servers:
            with MCPToolManager(
                command=each["command"], args=each["args"], env=each.get("env", None)
            ) as mcp_client:
                for each in mcp_client.get_tools_by_name(tools):
                    all_mcp_tools.append(each)

        for each in all_mcp_tools:
            print(each)
            roulette_agent.tool_plain(each)

        with FunctionToolManager() as function_client:
            for each in function_client.get_tools_by_name(tools):
                roulette_agent.tool_plain(each)

        result = roulette_agent.run_sync(prompt)

        return result.data


Call = CallManager()
