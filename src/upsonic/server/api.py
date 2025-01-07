from fastapi import FastAPI, HTTPException
from functools import wraps
import asyncio

app = FastAPI()


def timeout(duration: float):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=duration)
            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=408,
                    detail=f"Operation timed out after {duration} seconds",
                )
            except Exception as e:
                raise e

        return wrapper

    return decorator
