from pydantic import BaseModel


from typing import Any, List, Dict, Optional, Type, Union


from .task_response import CustomTaskResponse, ObjectResponse

class Task(BaseModel):
    description: str
    response_format: Union[Type[CustomTaskResponse], Type[ObjectResponse], Any] = None
    _response: Any = None

    @property
    def response(self):
        if type(self._response) == str:
            return self._response

        if self._response._upsonic_response_type == "custom":
            return self._response.output()
        else:
            return self._response



