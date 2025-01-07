import httpx
from typing import Dict, List, Any, Callable, Optional


class MCPToolManager:
    """Client for interacting with the Upsonic MCP Tools API."""

    def __init__(
        self, command: str, args: List[str], env: dict[str, str] | None = None
    ):
        """
        Initialize the Upsonic client.

        Args:
            command: The command to execute
            args: List of command arguments
        """
        self.base_url = "http://127.0.0.1:8086"
        self.command = command
        self.args = args
        self.env = env

    def get_tools_by_name(self, name: list[str]):
        """
        Get tools by name
        """
        return [tool for tool in self.tools() if tool.__name__ in name]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # No longer needed as we use context managers

    def close(self):
        """Close the client session."""
        pass  # No longer needed as we use context managers

    def list_tools(self) -> Dict[str, Any]:
        """List all available tools."""
        # Create a fresh client for each call
        with httpx.Client(timeout=600.0) as session:
            response = session.post(
                f"{self.base_url}/mcp/tools",
                json={"command": self.command, "args": self.args, "env": self.env},
            )
            response.raise_for_status()
            return response.json()

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a specific tool with the given arguments.

        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments to pass to the tool

        Returns:
            Tool execution results
        """
        # Create a fresh client for each call
        with httpx.Client(timeout=600.0) as session:
            response = session.post(
                f"{self.base_url}/mcp/call_tool",
                json={
                    "command": self.command,
                    "args": self.args,
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "env": self.env,
                },
            )
            response.raise_for_status()
            return response.json()

    def tools(self) -> List[Callable[..., Dict[str, Any]]]:
        """Initialize tool-specific methods based on available tools."""
        tools_response: ListToolsResponse = self.list_tools()
        tools = tools_response.get("available_tools", {}).get("tools", [])

        # Create a list to store the functions
        functions: List[Callable[..., Dict[str, Any]]] = []

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

        for tool in tools:
            tool_name: str = tool["name"]
            tool_desc: str = tool.get("description", "")
            input_schema: Dict[str, Any] = tool.get("inputSchema", {})
            properties: Dict[str, Dict[str, Any]] = input_schema.get("properties", {})
            required: List[str] = input_schema.get("required", [])

            # Create the wrapper function with proper type annotations
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

                def tool_function(*args: Any, **kwargs: Any) -> Dict[str, Any]:
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

                    # Validate required parameters
                    for req in required:
                        if req not in all_kwargs:
                            raise ValueError(f"Missing required parameter: {req}")

                    # Add defaults for optional parameters
                    for param, default in defaults.items():
                        if param not in all_kwargs:
                            all_kwargs[param] = default

                    # Deugging
                    print()
                    print("all_kwargs", all_kwargs)
                    print("tool_name", tool_name)
                    print()

                    return self.call_tool(tool_name, all_kwargs)

                # Set function name and annotations
                tool_function.__name__ = tool_name
                tool_function.__annotations__ = {
                    **annotations,
                    "return": Dict[str, Any],
                }
                tool_function.__doc__ = (
                    f"{tool_desc}\n\nReturns:\n    Tool execution results"
                )

                return tool_function

            # Create function with proper annotations
            func = create_tool_function(tool_name, properties, required)

            # Add the function to the class instance without binding self
            functions.append(func)

        # return the functions
        return functions
