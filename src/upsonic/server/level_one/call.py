from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from pydantic import BaseModel
from pydantic_ai.result import ResultData

from ...storage.configuration import Configuration

from ..tools.mcp_client import MCPToolManager
from ..tools.function_client import FunctionToolManager


class CallManager:
    def gpt_4o(
        self,
        prompt: str,
        response_format: BaseModel = str,
        tools: list[str] = [],
        mcp_servers: list[dict[str, str]] = [],
    ) -> ResultData:
        model = OpenAIModel("gpt-4o", api_key=Configuration.get("OPENAI_API_KEY"))
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
