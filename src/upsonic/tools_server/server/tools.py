import base64
import subprocess
import traceback
import asyncio
from typing import List, Dict, Any, Optional, Union, Callable
from pydantic import BaseModel



from fastapi import HTTPException
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.stdio import get_default_environment
import asyncio
from contextlib import asynccontextmanager
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


def install_library_(library):
    try:
        result = subprocess.run(
            ["uv", "pip", "install", library],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        traceback.print_exc()
        return False


def uninstall_library_(library):
    try:
        result = subprocess.run(
            ["uv", "pip", "uninstall", "-y", library],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        traceback.print_exc()
        return False
    

def add_tool_(function, description: str = "", properties: Dict[str, Any] = {}, required: List[str] = []):
    """
    Add a tool to the registered functions.
    
    Args:
        function: The function to be registered as a tool
    """
    from ..server.function_tools import tool
    # Apply the tool decorator with empty description

    # ANalyze the functino signature
    print("function", function)
    print("function.__annotations__", function.__annotations__)

    
    decorated_function = tool(description=description, custom_properties=properties, custom_required=required)(function)
    return decorated_function

    






import cloudpickle
from fastapi import HTTPException
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters

import asyncio
from contextlib import asynccontextmanager
# Create server parameters for stdio connection

from .api import app, timeout


prefix = "/tools"


class InstallLibraryRequest(BaseModel):
    library: str



@app.post(f"{prefix}/install_library")
async def install_library(request: InstallLibraryRequest):
    """
    Endpoint to install a library.

    Args:
        library: The library to install

    Returns:
        A success message
    """

    print("install_library", request)
    install_library_(request.library)
    print("install_library done")
    return {"message": "Library installed successfully"}



@app.post(f"{prefix}/uninstall_library")
async def uninstall_library(request: InstallLibraryRequest):
    """
    Endpoint to uninstall a library.
    """
    uninstall_library_(request.library)
    return {"message": "Library uninstalled successfully"}





class AddToolRequest(BaseModel):
    function: str

@app.post(f"{prefix}/add_tool")
async def add_tool(request: AddToolRequest):
    """
    Endpoint to add a tool.
    """
    # Cloudpickle the function
    decoded_function = base64.b64decode(request.function)
    deserialized_function = cloudpickle.loads(decoded_function)

    add_tool_(deserialized_function)
    return {"message": "Tool added successfully"}



class AddMCPToolRequest(BaseModel):
    command: str
    args: List[str]
    env: Dict[str, str]


async def add_mcp_tool_(command: str, args: List[str], env: Dict[str, str]):
    """
    Add a tool.
    """
    def get_python_type(schema_type: str, format: Optional[str] = None) -> type:
        """Convert JSON schema type to Python type."""
        type_mapping = {
            "string": str,
            "integer": int,
            "boolean": bool,
            "number": float,
            "array": list,
            "object": dict,
        }
        return type_mapping.get(schema_type, Any)

    async with managed_session(command=command, args=args, env=env) as session:
        tools = await session.list_tools()

        tools = tools.tools
        for tool in tools:
            print("\n\n")
            print("tool", tool)
            tool_name: str = tool.name
            tool_desc: str = tool.description
            input_schema: Dict[str, Any] = tool.inputSchema
            properties: Dict[str, Dict[str, Any]] = input_schema.get("properties", {})
            required: List[str] = input_schema.get("required", [])

            def create_tool_function(
                tool_name: str,
                properties: Dict[str, Dict[str, Any]],
                required: List[str],
            ) -> Callable[..., Dict[str, Any]]:
                # Create function parameters type annotations
                annotations = {}
                defaults = {}

                # First add required parameters
                for param_name in required:
                    param_info = properties[param_name]
                    param_type = get_python_type(param_info.get("type", "any"))
                    annotations[param_name] = param_type

                # Then add optional parameters
                for param_name, param_info in properties.items():
                    if param_name not in required:
                        param_type = get_python_type(param_info.get("type", "any"))
                        annotations[param_name] = param_type
                        defaults[param_name] = param_info.get("default", None)

                async def tool_function(*args: Any, **kwargs: Any) -> Dict[str, Any]:
                    print("\n=== Tool Function Debug ===")
                    print(f"Tool Name: {tool_name}")
                    print(f"Args: {args}")
                    print(f"Kwargs: {kwargs}")
                    print(f"Required Parameters: {required}")
                    print(f"Command: {tool_function.command}")
                    print(f"Command Args: {tool_function.args}")
                    print(f"Environment: {tool_function.env}")

                    # Convert positional args to kwargs
                    if len(args) > len(required):
                        raise TypeError(
                            f"{tool_name}() takes {len(required)} positional arguments but {len(args)} were given"
                        )

                    # Combine positional args with kwargs
                    all_kwargs = kwargs.copy()
                    for i, arg in enumerate(args):
                        if i < len(required):
                            all_kwargs[required[i]] = arg

                    print(f"Combined kwargs: {all_kwargs}")

                    # Validate required parameters
                    for req in required:
                        if req not in all_kwargs:
                            raise ValueError(f"Missing required parameter: {req}")

                    # Add defaults for optional parameters
                    for param, default in defaults.items():
                        if param not in all_kwargs:
                            all_kwargs[param] = default

                    print(f"Final kwargs with defaults: {all_kwargs}")

                    # Create a new session for each call using the function's stored parameters
                    print("Creating new session...")
                    async with managed_session(command=tool_function.command, args=tool_function.args, env=tool_function.env) as new_session:
                        print("Calling tool...", tool_function.command, tool_function.args, tool_function.env, tool_name)
                        print("all_kwargs", all_kwargs)

                        # Remove None kwargs
                        all_kwargs = {k: v for k, v in all_kwargs.items() if v is not None}

                        result = await new_session.call_tool(name=tool_name, arguments=all_kwargs)
                        print(f"Tool result: {result}")
                        print("=== End Tool Function Debug ===\n")
                        return {"result": result}

                # Set function name and annotations
                tool_function.__name__ = tool_name
                tool_function.__annotations__ = {
                    **annotations,
                    "return": Dict[str, Any],
                }
                tool_function.__doc__ = (
                    f"{tool_desc}\n\nReturns:\n    Tool execution results"
                )

                # Store session parameters as attributes of the function
                tool_function.command = command
                tool_function.args = args
                tool_function.env = env

                # Print the required parameters
                print("required", required)

                return tool_function

            # Create function with proper annotations
            func = create_tool_function(tool_name, properties, required)
            add_tool_(func, description=tool_desc, properties=properties, required=required)


@app.post(f"{prefix}/add_mcp_tool")
async def add_mcp_tool(request: AddMCPToolRequest):
    """
    Endpoint to add a tool.
    """
    await add_mcp_tool_(request.command, request.args, request.env)
    return {"message": "Tool added successfully"}