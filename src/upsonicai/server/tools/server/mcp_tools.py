from fastapi import HTTPException
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.stdio import get_default_environment
# Create server parameters for stdio connection

from .api import app, timeout


prefix = "/mcp"


class BaseRequestMCP(BaseModel):
    command: str
    args: list[str]
    env: dict[str, str] | None = None


class ToolRequest(BaseRequestMCP):
    tool_name: str
    arguments: dict


class ListToolsRequest(BaseRequestMCP):
    pass


async def get_session(command: str, args: list, env: dict):
    print("env", env)
    print("args", args)
    print("command", command)

    if env:
        env = get_default_environment()
        env.update(env) if env else None

    server_params = StdioServerParameters(
        command=command,  # Executable
        args=args,  # Optional command line arguments
        env=env,  # Environment variables
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session
            await session.close()


@app.post(f"{prefix}/tools")
@timeout(30.0)
async def list_tools(request: ListToolsRequest):
    print("Listing tools...")

    async for session in get_session(request.command, request.args, request.env):
        try:
            tools = await session.list_tools()
            print(f"Tools listed: {tools}")
        except Exception as e:
            print(f"Error listing tools: {e}")
            raise HTTPException(status_code=500, detail="Failed to list tools")
        return {"available_tools": tools}


@app.post(f"{prefix}/call_tool")
@timeout(30.0)
async def call_tool(request: ToolRequest):
    print(f"Received tool call request: {request}")

    async for session in get_session(request.command, request.args, request.env):
        try:
            print(
                f"Calling tool: {request.tool_name} with arguments: {request.arguments}"
            )
            result = await session.call_tool(
                request.tool_name, arguments=request.arguments
            )
            print(f"Tool call result: {result}")
        except Exception as e:
            print(f"Error calling tool: {e}")
            raise HTTPException(status_code=500, detail="Failed to call tool")
        return {"result": result}
