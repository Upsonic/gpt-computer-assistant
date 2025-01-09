import cloudpickle
import dill
import base64
import httpx
from typing import Any, List, Dict, Optional, Type, Union
from pydantic import BaseModel

from ..tasks.tasks import Task

class NoAPIKeyException(Exception):
    pass

class UnsupportedLLMModelException(Exception):
    pass


class Tools:

    def tool(
        self,
        function,
    ) -> Any:

        # Get the function then make a cloudpickle of it

        the_module = dill.detect.getmodule(function)
        if the_module is not None:
            cloudpickle.register_pickle_by_value(the_module)

        the_dumped_function = cloudpickle.dumps(function)

        data = {
            "function": base64.b64encode(the_dumped_function).decode("utf-8"),
            "name": function.__name__,
        }
        
        result = self.send_request("/tool/add_mcp_server", data)

    def install_library(self, library: str) -> Dict[str, Any]:
        result = self.send_request("/tools/install_library", {"library": library})
        return result

    def uninstall_library(self, library: str) -> Dict[str, Any]:
        result = self.send_request("/tools/uninstall_library", {"library": library})
        return result
