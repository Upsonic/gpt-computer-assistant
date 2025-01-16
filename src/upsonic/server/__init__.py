from ..storage.configuration import Configuration
from .level_one.call import Call

from .api import app
from .level_one.server.server import *
from .level_two.server.server import *
from .storage.server.server import *
from .tools.server import *
from .markdown.server.server import *
from .others.server.server import *

import warnings
import uvicorn
import multiprocessing
import signal
import time
import os
import sys
from typing import Optional
from multiprocessing import freeze_support

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

_server_process: Optional[multiprocessing.Process] = None

def _setup_log_directory():
    """Create logs directory if it doesn't exist"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def _run_server(redirect_output: bool = False):
    """Run the server process with the specified configuration."""
    if redirect_output:
        log_dir = _setup_log_directory()
        sys.stdout = open(os.path.join(log_dir, 'main_server.log'), 'a')
        sys.stderr = open(os.path.join(log_dir, 'main_server_error.log'), 'a')
    
    def handle_signal(signum, frame):
        sys.exit(0)
        
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    
    config = uvicorn.Config(
        "upsonic.server.api:app", 
        host="localhost", 
        port=7541,
        log_level="error",
        access_log=False
    )
    server = uvicorn.Server(config)
    server.run()

def run_main_server(redirect_output: bool = False):
    """Start the main server if it's not already running."""
    global _server_process
    
    if _server_process is not None and _server_process.is_alive():
        return

    if sys.platform == 'darwin':
        multiprocessing.set_start_method('spawn', force=True)
    else:
        multiprocessing.set_start_method('fork', force=True)

    _server_process = multiprocessing.Process(target=_run_server, args=(redirect_output,))
    _server_process.daemon = True
    _server_process.start()
    time.sleep(1)  # Give the server a moment to start

def run_main_server_internal(reload: bool = True):
    uvicorn.run("upsonic.server.api:app", host="0.0.0.0", port=7541, reload=reload)

def stop_main_server():
    """Stop the main server if it's running."""
    global _server_process
    if _server_process is None or not _server_process.is_alive():
        return
    
    _server_process.terminate()
    _server_process.join()
    _server_process = None

def is_main_server_running() -> bool:
    """Check if the main server is currently running."""
    global _server_process
    return _server_process is not None and _server_process.is_alive()

from ..tools_server import run_tools_server, stop_tools_server, is_tools_server_running

def run_dev_server():
    if sys.platform == 'darwin':
        multiprocessing.set_start_method('spawn', force=True)
    else:
        multiprocessing.set_start_method('fork', force=True)
    run_main_server(redirect_output=True)
    run_tools_server(redirect_output=True)
    while not is_main_server_running() or not is_tools_server_running():
        time.sleep(1)

def stop_dev_server():
    stop_main_server()
    stop_tools_server()

if __name__ == '__main__':
    freeze_support()

__all__ = ["hello", "Configuration", "Call", "app", "run_main_server", "stop_main_server", "is_main_server_running", "run_main_server_internal"]
