from pydantic import BaseModel
from typing import Dict, Any, Any
import httpx


from .level_one.call import Call
from .storage.storage import Storage


class ServerStatusException(Exception):
    """Custom exception for server status check failures."""
    pass

# Create a base class with url
class UpsonicServer(Call, Storage):


    def __init__(self, url: str):
        self.url = url
        if not self.status():
            raise ServerStatusException("Failed to connect to the server at initialization.")

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

            response = client.post(self.url + endpoint, json=data)
            response.raise_for_status()
            return response.json()