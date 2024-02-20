from pydantic import BaseModel
from typing import List
from app.users.schemas import SUser

class RoleSchema(BaseModel):
    id: int
    description: str
    users: List[SUser]

    class Config:
        from_attributes = True