from pydantic import BaseModel
from typing import List, Optional

from app.messages.schemas import SMessage

class SUser(BaseModel):
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

class SUserForTicket(BaseModel):
    surname: str
    name: str
    secname: str
    contact_tel: Optional[str]

    class Config:
        from_attributes = True