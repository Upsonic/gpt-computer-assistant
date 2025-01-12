import uvicorn
import multiprocessing
import signal
import time
from typing import Optional

_server_process: Optional[multiprocessing.Process] = None

def run_tools_server():
    """Start the tools server if it's not already running."""
    global _server_process
    
    if _server_process is not None and _server_process.is_alive():

        return

    def run_server():
        # Ignore SIGTERM in child process to prevent signal handler conflicts
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        config = uvicorn.Config(
            "upsonic.tools_server.server.api:app", 
            host="0.0.0.0", 
            port=8086,
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




def run_tools_server_internal():
    uvicorn.run("upsonic.tools_server.server.api:app", host="0.0.0.0", port=8086, reload=True)


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

__all__ = ["run_tools_server", "stop_tools_server", "is_tools_server_running", "app", "run_tools_server_internal"]
