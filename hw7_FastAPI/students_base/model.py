from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    group: str
    grades: list[Grade]

class Grade(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    value: Literal[1,2,3,4,5]