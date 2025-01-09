import subprocess
import traceback


def install_library_(library):
    try:
        result = subprocess.run(
            ["pip", "install", library],
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
            ["pip", "uninstall", "-y", library],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        traceback.print_exc()
        return False
    

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
