from typing import Optional
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True