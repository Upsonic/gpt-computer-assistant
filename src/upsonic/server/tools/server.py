from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
import traceback
from ..api import app, timeout
from ...tools_server.tools_client import ToolManager
import asyncio
from concurrent.futures import ThreadPoolExecutor
import cloudpickle
import base64


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
    with ToolManager() as tool_client:
        tool_client.install_library(request.library)
    return {"message": "Library installed successfully"}



@app.post(f"{prefix}/uninstall_library")
async def uninstall_library(request: InstallLibraryRequest):
    """
    Endpoint to uninstall a library.
    """
    with ToolManager() as tool_client:
        tool_client.uninstall_library(request.library)
    return {"message": "Library uninstalled successfully"}
