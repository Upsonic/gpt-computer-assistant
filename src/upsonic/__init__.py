from .client.base import UpsonicClient
from .client.tasks.task_response import ObjectResponse, StrResponse, IntResponse, FloatResponse, BoolResponse, StrInListResponse
from .client.tasks.tasks import Task



def hello() -> str:
    return "Hello from upsonic!"


__all__ = ["hello", "UpsonicClient", "ObjectResponse", "StrResponse", "IntResponse", "FloatResponse", "BoolResponse", "Task", "StrInListResponse"]
