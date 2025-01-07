from fastapi import FastAPI, HTTPException
import asyncio
from functools import wraps

app = FastAPI()


class TimeoutException(Exception):
    pass


async def timeout_handler(duration: float, coro):
    try:
        return await asyncio.wait_for(coro, timeout=duration)
    except asyncio.TimeoutError:
        raise TimeoutException(f"Operation timed out after {duration} seconds")


# Timeout decorator
def timeout(duration: float):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f"Starting execution of {func.__name__} with timeout {duration} seconds")
            try:
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=duration)
                print(f"Execution of {func.__name__} completed successfully")
                return result
            except asyncio.TimeoutError:
                print(f"Execution of {func.__name__} timed out after {duration} seconds")
                raise HTTPException(
                    status_code=408,
                    detail=f"Operation timed out after {duration} seconds",
                )

        return wrapper

    return decorator
