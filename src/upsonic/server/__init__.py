from ..storage.configuration import Configuration
from .level_one.call import Call


from .api import app
from .level_one.server.server import *
from .storage.server.server import *


import warnings

warnings.filterwarnings("ignore", category=UserWarning)


import uvicorn

def run_main_server():
    uvicorn.run("upsonic.server.api:app", host="0.0.0.0", port=7541, reload=True)




__all__ = ["hello", "Configuration", "Call", "app"]
