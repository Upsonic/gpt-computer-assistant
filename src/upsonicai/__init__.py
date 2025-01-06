from .client.base import UpsonicClient


def hello() -> str:
    return "Hello from upsonicai!"


__all__ = ["hello", "UpsonicClient"]
