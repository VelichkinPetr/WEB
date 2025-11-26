from typing import Optional
from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    author: str
    year: Optional[int] = None
    in_stock: bool = True