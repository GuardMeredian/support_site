from pydantic import BaseModel
from typing import List
from app.users.schemas import UserSchema

class RoleSchema(BaseModel):
    id: int
    description: str
    users: List[UserSchema]

    class Config:
        orm_mode = True