import base64
import subprocess
import traceback


def install_library_(library):
    try:
        result = subprocess.run(
            ["uv", "pip", "install", library],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        traceback.print_exc()
        return False


def uninstall_library_(library):
    try:
        result = subprocess.run(
            ["uv", "pip", "uninstall", "-y", library],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        traceback.print_exc()
        return False
    

def add_tool_(function):
    """
    Add a tool to the registered functions.
    
    Args:
        function: The function to be registered as a tool
    """
    from ..server.function_tools import tool
    # Apply the tool decorator with empty description
    decorated_function = tool()(function)
    return decorated_function

    






import cloudpickle
from fastapi import HTTPException
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters

import asyncio
from contextlib import asynccontextmanager
# Create server parameters for stdio connection

from .api import app, timeout


prefix = "/tools"


class InstallLibraryRequest(BaseModel):
    library: str



@app.post(f"{prefix}/install_library")
async def install_library(request: InstallLibraryRequest):
    """
    Endpoint to install a library.

    Args:
        library: The library to install

    Returns:
        A success message
    """

    print("install_library", request)
    install_library_(request.library)
    print("install_library done")
    return {"message": "Library installed successfully"}



@app.post(f"{prefix}/uninstall_library")
async def uninstall_library(request: InstallLibraryRequest):
    """
    Endpoint to uninstall a library.
    """
    uninstall_library_(request.library)
    return {"message": "Library uninstalled successfully"}





class AddToolRequest(BaseModel):
    function: str

@app.post(f"{prefix}/add_tool")
async def add_tool(request: AddToolRequest):
    """
    Endpoint to add a tool.
    """
    # Cloudpickle the function
    decoded_function = base64.b64decode(request.function)
    deserialized_function = cloudpickle.loads(decoded_function)

    add_tool_(deserialized_function)
    return {"message": "Tool added successfully"}
