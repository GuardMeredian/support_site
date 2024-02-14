from pydantic import BaseModel
from typing import Optional

class OrganizationSchema(BaseModel):
    id: Optional[int] = None
    lpucode: int
    name: str

    class Config:
        orm_mode = True