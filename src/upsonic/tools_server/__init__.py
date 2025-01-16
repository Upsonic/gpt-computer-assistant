import uvicorn
import multiprocessing
import signal
import time
import os
import sys
from typing import Optional
from multiprocessing import freeze_support

_server_process: Optional[multiprocessing.Process] = None

def _setup_log_directory():
    """Create logs directory if it doesn't exist"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def _run_server(redirect_output: bool = False):
    """Run the tools server process with the specified configuration."""
    if redirect_output:
        log_dir = _setup_log_directory()
        sys.stdout = open(os.path.join(log_dir, 'tools_server.log'), 'a')
        sys.stderr = open(os.path.join(log_dir, 'tools_server_error.log'), 'a')
    
    def handle_signal(signum, frame):
        sys.exit(0)
        
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    
    config = uvicorn.Config(
        "upsonic.tools_server.server.api:app", 
        host="localhost", 
        port=8086,
        log_level="error",
        access_log=False
    )
    server = uvicorn.Server(config)
    server.run()

def run_tools_server(redirect_output: bool = False):
    """Start the tools server if it's not already running."""
    global _server_process
    
    if _server_process is not None and _server_process.is_alive():
        return

    if sys.platform == 'darwin':
        multiprocessing.set_start_method('fork', force=True)

    _server_process = multiprocessing.Process(target=_run_server, args=(redirect_output,))
    _server_process.daemon = True
    _server_process.start()
    time.sleep(1)  # Give the server a moment to start

def run_tools_server_internal(reload: bool = True):
    uvicorn.run("upsonic.tools_server.server.api:app", host="localhost", port=8086, reload=reload)

def stop_tools_server():
    """Stop the tools server if it's running."""
    global _server_process
    if _server_process is None or not _server_process.is_alive():
        return
    
    _server_process.terminate()
    _server_process.join()
    _server_process = None

def is_tools_server_running() -> bool:
    """Check if the tools server is currently running."""
    global _server_process
    return _server_process is not None and _server_process.is_alive()

if __name__ == '__main__':
    freeze_support()

__all__ = ["run_tools_server", "stop_tools_server", "is_tools_server_running", "app", "run_tools_server_internal"]
