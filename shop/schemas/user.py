from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    status: bool
    is_admin: bool

class User(UserCreate):
    id: int
    created_at: datetime
    updated_at: Annotated[datetime, None]

