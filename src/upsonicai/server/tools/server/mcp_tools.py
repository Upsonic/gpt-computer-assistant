from fastapi import HTTPException
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.stdio import get_default_environment
import asyncio
from contextlib import asynccontextmanager
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


@asynccontextmanager
async def managed_session(command: str, args: list, env: dict | None = None):
    print("env", env)
    print("args", args)
    print("command", command)

    if env is None:
        env = get_default_environment()
    else:
        default_env = get_default_environment()
        default_env.update(env)
        env = default_env

    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=env,
    )
    
    client = None
    session = None
    
    try:
        client = stdio_client(server_params)
        read, write = await client.__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        yield session
    finally:
        if session:
            try:
                await session.__aexit__(None, None, None)
            except Exception:
                pass
        if client:
            try:
                await client.__aexit__(None, None, None)
            except Exception:
                pass


@app.post(f"{prefix}/tools")
@timeout(30.0)
async def list_tools(request: ListToolsRequest):
    print("Listing tools...")
    
    try:
        async with managed_session(request.command, request.args, request.env) as session:
            tools = await session.list_tools()
            print(f"Tools listed: {tools}")
            return {"available_tools": tools}
    except asyncio.CancelledError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        print(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail="Failed to list tools")


@app.post(f"{prefix}/call_tool")
@timeout(30.0)
async def call_tool(request: ToolRequest):
    print(f"Received tool call request: {request}")
    
    try:
        async with managed_session(request.command, request.args, request.env) as session:
            print(f"Calling tool: {request.tool_name} with arguments: {request.arguments}")
            result = await session.call_tool(request.tool_name, arguments=request.arguments)
            print(f"Tool call result: {result}")
            return {"result": result}
    except asyncio.CancelledError:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        print(f"Error calling tool: {e}")
        raise HTTPException(status_code=500, detail="Failed to call tool")
