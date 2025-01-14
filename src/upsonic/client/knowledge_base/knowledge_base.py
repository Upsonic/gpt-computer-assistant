from dataclasses import Field
import uuid
from pydantic import BaseModel


from typing import Any, List, Dict, Optional, Type, Union






class KnowledgeBase(BaseModel):
    sources: List[str] = []

    def add_file(self, file_path: str):
        self.sources.append(file_path)

    def remove_file(self, file_path: str):
        self.sources.remove(file_path)