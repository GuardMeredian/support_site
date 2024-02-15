from pydantic import BaseModel
from typing import List, Optional

from app.messages.schemas import SMessage

class UserSchema(BaseModel):
    id: int
    login: str
    password: str
    surname: str
    name: str
    secname: str
    post: str
    email: Optional[str]
    contact_tel: Optional[str]
    organiztion_id: int
    role_id: int
    messages: Optional[List[SMessage]] = []

    class Config:
        from_attributes = True