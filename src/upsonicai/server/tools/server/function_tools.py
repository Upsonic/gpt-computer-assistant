from fastapi import HTTPException
from pydantic import BaseModel
import inspect
from typing import Any, Dict, List, Type, Callable
from functools import wraps

from .api import app, timeout

prefix = "/functions"

# Registry to store decorated functions
registered_functions: Dict[str, Dict[str, Any]] = {}


def _get_json_type(python_type: Type) -> str:
    """Convert Python type to JSON schema type."""
    type_mapping = {
        str: "string",
        int: "integer",
        bool: "boolean",
        float: "number",
        list: "array",
        dict: "object",
    }
    return type_mapping.get(python_type, "string")


def tool(description: str = "", required_params: List[str] = None):
    """
    Decorator to register a function as a tool.

    Args:
        description: Description of the tool
        required_params: List of required parameter names
    """

    def decorator(func: Callable):
        sig = inspect.signature(func)

        # Get parameter info
        properties = {}
        required = required_params or []

        for param_name, param in sig.parameters.items():
            param_type = (
                param.annotation if param.annotation != inspect.Parameter.empty else Any
            )
            param_default = (
                None if param.default == inspect.Parameter.empty else param.default
            )

            properties[param_name] = {
                "type": _get_json_type(param_type),
                "description": f"Parameter {param_name}",
            }

            if param_default is not None:
                properties[param_name]["default"] = param_default

        # Register the function
        registered_functions[func.__name__] = {
            "function": func,
            "description": description or func.__doc__ or "",
            "properties": properties,
            "required": required,
        }

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator


class ToolRequest(BaseModel):
    tool_name: str
    arguments: dict


@app.post(f"{prefix}/tools")
@timeout(30.0)
async def list_tools():
    print("Listing tools...")

    tools = []
    for name, info in registered_functions.items():
        tools.append(
            {
                "name": name,
                "description": info["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": info["properties"],
                    "required": info["required"],
                },
            }
        )

    return {"available_tools": {"tools": tools}}


@app.post(f"{prefix}/call_tool")
@timeout(30.0)
async def call_tool(request: ToolRequest):
    print(f"Received tool call request: {request}")

    if request.tool_name not in registered_functions:
        raise HTTPException(
            status_code=404, detail=f"Tool {request.tool_name} not found"
        )

    try:
        func = registered_functions[request.tool_name]["function"]
        result = await func(**request.arguments)
        print(f"Tool call result: {result}")
        return {"result": result}
    except Exception as e:
        print(f"Error calling tool: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to call tool: {str(e)}")


# Example decorated functions
@tool(description="Add two numbers together", required_params=["a", "b"])
async def add_numbers(a: int, b: int) -> int:
    return a + b


@tool(description="Concatenate two strings", required_params=["str1", "str2"])
async def concat_strings(str1: str, str2: str) -> str:
    return str1 + str2
