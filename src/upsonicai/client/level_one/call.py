import cloudpickle
import base64
import httpx
from typing import Any, List, Dict, Optional, Type
from pydantic import BaseModel


class Call:

    def gpt_4o(
        self,
        prompt: str,
        response_format: Any = None,
        tools: Optional[List[str]] = None,
        mcp_servers: Optional[List[Dict[str, str]]] = None,
    ) -> Any:
        """
        Call GPT-4 with optional tools and MCP servers.

        Args:
            prompt: The input prompt for GPT-4
            response_format: The expected response format (can be a type or Pydantic model)
            tools: Optional list of tool names to use
            mcp_servers: Optional list of MCP server configurations

        Returns:
            The response in the specified format
        """
        # Serialize the response format if it's a type or BaseModel
        if response_format is None:
            response_format_str = "str"
        elif isinstance(response_format, (type, BaseModel)):
            # If it's a Pydantic model or other type, cloudpickle and base64 encode it
            pickled_format = cloudpickle.dumps(response_format)
            response_format_str = base64.b64encode(pickled_format).decode("utf-8")
        else:
            response_format_str = "str"

        # Prepare the request data
        data = {
            "prompt": prompt,
            "response_format": response_format_str,
            "tools": tools or [],
            "mcp_servers": mcp_servers or [],
        }

        print(data)

        # Use the send_request method from the Base class
        result = self.send_request("/level_one/gpt4o", data)

        # Deserialize the result
        decoded_result = base64.b64decode(result["result"])
        deserialized_result = cloudpickle.loads(decoded_result)
        return deserialized_result
