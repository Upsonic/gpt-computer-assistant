from .client.base import UpsonicServer


def hello() -> str:
    return "Hello from upsonic!"


__all__ = ["hello", "UpsonicServer"]
