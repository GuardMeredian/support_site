from pydantic import BaseModel
from typing import List, Optional
from app.users.schemas import SUserForOrg

class OrganizationSchema(BaseModel):
    id: Optional[int] = None
    lpucode: int
    name: str

    class Config:
        from_attributes = True


class SOrgForTicket(BaseModel):
    lpucode: int

    class Config:
        from_attributes = True

class SOrgCard(BaseModel):
    lpucode: int
    name: str
    users: List[SUserForOrg]

    class Config:
        from_attributes = True