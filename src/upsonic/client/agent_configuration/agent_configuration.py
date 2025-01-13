from pydantic import BaseModel


from typing import Any, List, Dict, Optional, Type, Union




class AgentConfiguration(BaseModel):
    job_title: str
    company_url: str
    company_objective: str



