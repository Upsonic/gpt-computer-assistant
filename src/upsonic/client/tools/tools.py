import cloudpickle
import dill
import base64
import httpx
from typing import Any, List, Dict, Optional, Type, Union, Callable
from pydantic import BaseModel
from functools import wraps

from ..tasks.tasks import Task

class NoAPIKeyException(Exception):
    pass

class UnsupportedLLMModelException(Exception):
    pass


class Tools:
    def tool(self, library: Optional[Union[str, List[str]]] = None):
        """
        Decorator to register a function as a tool.
        Can be used as @tool(), @tool("pandas"), or @tool(["pandas", "numpy"])

        Args:
            library: Optional library name or list of library names to install before registering the tool
        """
        def decorator(func: Callable):
            # Install libraries first if specified
            if library:
                if isinstance(library, str):
                    self.install_library(library)
                else:
                    for lib in library:
                        self.install_library(lib)
            
            # Register the function as a tool
            self.add_tool(func)
            
            # Return the original function
            return func
        return decorator

    def add_tool(
        self,
        function,
    ) -> Any:

        # Get the function then make a cloudpickle of it

        the_module = dill.detect.getmodule(function)
        if the_module is not None:
            cloudpickle.register_pickle_by_value(the_module)

        the_dumped_function = cloudpickle.dumps(function)

        data = {
            "function": base64.b64encode(the_dumped_function).decode("utf-8"),
        }
        
        result = self.send_request("/tools/add_tool", data)
        return result
    


    def add_mcp_tool(self, command: str, args: List[str], env: Dict[str, str] = {}) -> Dict[str, Any]:
        result = self.send_request("/tools/add_mcp_tool", {"command": command, "args": args, "env": env})
        return result

    def install_library(self, library: str) -> Dict[str, Any]:
        result = self.send_request("/tools/install_library", {"library": library})
        return result

    def uninstall_library(self, library: str) -> Dict[str, Any]:
        result = self.send_request("/tools/uninstall_library", {"library": library})
        return result

    def mcp(self):
        """
        Decorator to register a class as an MCP tool.
        Usage:
        @client.mcp()
        class ToolName:
            command = "command-name"
            args = ["arg1", "arg2"]
            env = {"key": "value"}
        """
        def decorator(cls):
            command = getattr(cls, "command", None)
            args = getattr(cls, "args", [])
            env = getattr(cls, "env", {})
            
            if not command:
                raise ValueError("MCP tool class must have a 'command' attribute")
                
            self.add_mcp_tool(command, args, env)
            return cls
        return decorator
