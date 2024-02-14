from pydantic import BaseModel
from typing import Optional

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

    class Config:
        orm_mode = True