from pydantic import BaseModel
from typing import List, Optional



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

    class Config:
        from_attributes = True

class SUserForTicket(BaseModel):
    id: int
    surname: str
    name: str
    secname: str
    contact_tel: str

    class Config:
        from_attributes = True


class SUserForOrg(BaseModel):
    surname: str
    name: str
    secname: str
    post:str
    contact_tel: str

    class Config:
        from_attributes = True


class SUserAuth(BaseModel):
    login:str
    password:str

    class Config:
        from_attributes = True

class SUserForMsg(BaseModel):
    id: int
    surname: str
    name: str
    secname: str

    class Config:
        from_attributes = True