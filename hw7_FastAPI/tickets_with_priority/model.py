from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict


class Ticket(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "closed"]
