import multiprocessing
import os
import signal
import sys
import time
import uvicorn
from typing import Optional
import psutil
import socket
from contextlib import closing

class ServerManager:
    def __init__(self, app_path: str, host: str, port: int, name: str):
        self.app_path = app_path
        self.host = host
        self.port = port
        self.name = name
        self._process: Optional[multiprocessing.Process] = None
        self._pid_file = os.path.join(os.path.expanduser("~"), f".upsonic_{name}_server.pid")

    def _setup_log_directory(self):
        """Create logs directory if it doesn't exist"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def _is_port_in_use(self) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex((self.host, self.port)) == 0

    def _write_pid(self):
        """Write the current process ID to the PID file"""
        if self._process:
            with open(self._pid_file, 'w') as f:
                f.write(str(self._process.pid))

    def _read_pid(self) -> Optional[int]:
        """Read the process ID from the PID file"""
        try:
            if os.path.exists(self._pid_file):
                with open(self._pid_file, 'r') as f:
                    return int(f.read().strip())
        except (ValueError, IOError):
            pass
        return None

    def _cleanup_pid(self):
        """Remove the PID file"""
        try:
            if os.path.exists(self._pid_file):
                os.remove(self._pid_file)
        except OSError:
            pass

    def _run_server(self, redirect_output: bool = False):
        """Run the server process with the specified configuration."""
        if redirect_output:
            log_dir = self._setup_log_directory()
            sys.stdout = open(os.path.join(log_dir, f'{self.name}_server.log'), 'a')
            sys.stderr = open(os.path.join(log_dir, f'{self.name}_server_error.log'), 'a')
        
        def handle_signal(signum, frame):
            sys.exit(0)
            
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)
        
        config = uvicorn.Config(
            self.app_path,
            host=self.host,
            port=self.port,
            log_level="error",
            access_log=False
        )
        server = uvicorn.Server(config)
        server.run()

    def start(self, redirect_output: bool = False):
        """Start the server if it's not already running."""
        if self.is_running():
            return

        # Check if port is already in use
        if self._is_port_in_use():
            raise RuntimeError(f"Port {self.port} is already in use")

        # Set up multiprocessing based on platform
        if sys.platform == 'darwin':
            multiprocessing.set_start_method('fork', force=True)
        elif sys.platform == 'win32':
            multiprocessing.set_start_method('spawn', force=True)

        self._process = multiprocessing.Process(
            target=self._run_server,
            args=(redirect_output,),
            name=f"upsonic_{self.name}_server"
        )
        self._process.daemon = True
        self._process.start()
        self._write_pid()
        
        # Wait for server to start
        start_time = time.time()
        while not self._is_port_in_use() and time.time() - start_time < 10:
            if not self._process.is_alive():
                raise RuntimeError(f"Failed to start {self.name} server")
            time.sleep(0.1)

    def stop(self):
        """Stop the server if it's running."""
        pid = self._read_pid()
        if pid:
            try:
                process = psutil.Process(pid)
                process.terminate()
                process.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                pass

        if self._process and self._process.is_alive():
            self._process.terminate()
            self._process.join(timeout=5)
            if self._process.is_alive():
                self._process.kill()

        self._process = None
        self._cleanup_pid()

    def is_running(self) -> bool:
        """Check if the server is currently running."""
        if self._process and self._process.is_alive():
            return True

        pid = self._read_pid()
        if pid:
            try:
                process = psutil.Process(pid)
                return process.is_running() and process.name().startswith("python")
            except psutil.NoSuchProcess:
                self._cleanup_pid()
        return False 