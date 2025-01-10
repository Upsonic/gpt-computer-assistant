from pydantic import BaseModel
from typing import Dict, Any, Any
import httpx


from .level_one.call import Call
from .storage.storage import Storage
from .tools.tools import Tools


class ServerStatusException(Exception):
    """Custom exception for server status check failures."""
    pass

class TimeoutException(Exception):
    """Custom exception for request timeout."""
    pass

# Create a base class with url
class UpsonicClient(Call, Storage, Tools):


    def __init__(self, url: str):
        self.url = url
        self.default_llm_model = "gpt-4o"
        if not self.status():
            raise ServerStatusException("Failed to connect to the server at initialization.")


    def set_default_llm_model(self, llm_model: str):
        self.default_llm_model = llm_model


    def status(self) -> bool:
        """Check the server status."""
        try:
            with httpx.Client() as client:
                response = client.get(self.url + "/status")
                return response.status_code == 200
        except httpx.RequestError:
            return False

    def send_request(self, endpoint: str, data: Dict[str, Any]) -> Any:
        """
        General method to send an API request.

        Args:
            endpoint: The API endpoint to send the request to.
            data: The data to send in the request.

        Returns:
            The response from the API.
        """
        with httpx.Client() as client:

            response = client.post(self.url + endpoint, json=data, timeout=600.0)
            if response.status_code == 408:
                raise TimeoutException("Request timed out")
            response.raise_for_status()
            return response.json()