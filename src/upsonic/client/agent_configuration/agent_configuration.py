from dataclasses import Field
import uuid
from pydantic import BaseModel


from typing import Any, List, Dict, Optional, Type, Union




class AgentConfiguration(BaseModel):
    agent_id_: str = None
    job_title: str
    company_url: str
    company_objective: str

    sub_task: bool = False

    retries: int = 1

    memory: bool = False



    @property
    def agent_id(self):
        if self.agent_id_ is None:
            self.agent_id_ = str(uuid.uuid4())
        return self.agent_id_