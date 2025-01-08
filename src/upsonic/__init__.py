from .client.base import UpsonicClient
from pydantic import BaseModel

def hello() -> str:
    return "Hello from upsonic!"


__all__ = ["hello", "UpsonicClient", "BaseModel"]
