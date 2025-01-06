from pydantic import BaseModel
from typing import Dict, Any, Any
import httpx


from .level_one.call import Call


# Create a base class with url
class UpsonicClient(Call):


    def __init__(self, url: str):
        self.url = url

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