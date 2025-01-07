import cloudpickle
import dill
import base64
import httpx
from typing import Any, List, Dict, Optional, Type, Union
from pydantic import BaseModel


class Storage:



    def get_config(self, key: str) -> Any:
        """
        Get a configuration value by key from the server.

        Args:
            key: The configuration key

        Returns:
            The configuration value
        """
        data = {"key": key}
        response = self.send_request("/storage/config/get", data=data)
        return response.get("value")

    def set_config(self, key: str, value: str) -> str:
        """
        Set a configuration value on the server.

        Args:
            key: The configuration key
            value: The configuration value

        Returns:
            A success message
        """
        data = {"key": key, "value": value}
        response = self.send_request("/storage/config", data=data)
        return response.get("message")
