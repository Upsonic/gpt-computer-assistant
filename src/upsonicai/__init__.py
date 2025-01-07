from .client.base import UpsonicServer


def hello() -> str:
    return "Hello from upsonicai!"


__all__ = ["hello", "UpsonicServer"]
