from ..storage.configuration import Configuration
from .level_one.call import Call

from .api import app
from .level_one.server.server import *
from .storage.server.server import *
from .tools.server import *

import warnings
import uvicorn
import multiprocessing
import signal
import time
from typing import Optional

warnings.filterwarnings("ignore", category=UserWarning)

_server_process: Optional[multiprocessing.Process] = None

def run_main_server():
    """Start the main server if it's not already running."""
    global _server_process
    
    if _server_process is not None and _server_process.is_alive():

        return

    def run_server():
        # Ignore SIGTERM in child process to prevent signal handler conflicts
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        config = uvicorn.Config(
            "upsonic.server.api:app", 
            host="0.0.0.0", 
            port=7541,
            log_level="error",
            access_log=False
        )
        server = uvicorn.Server(config)
        server.run()
    
    if multiprocessing.get_start_method(allow_none=True) != 'fork':
        multiprocessing.set_start_method('fork', force=True)
    
    _server_process = multiprocessing.Process(target=run_server)
    _server_process.daemon = True  # Make process daemon so it exits when parent exits
    _server_process.start()
    time.sleep(2)  # Give the server a moment to start


def run_main_server_internal():
    uvicorn.run("upsonic.server.api:app", host="0.0.0.0", port=7541, reload=True)



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
    run_main_server()
    run_tools_server()

    while not is_main_server_running() or not is_tools_server_running():
        time.sleep(1)


    
def stop_dev_server():
    stop_main_server()
    stop_tools_server()


__all__ = ["hello", "Configuration", "Call", "app", "run_main_server", "stop_main_server", "is_main_server_running", "run_main_server_internal"]
