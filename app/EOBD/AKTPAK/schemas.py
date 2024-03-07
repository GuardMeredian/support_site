from pydantic import BaseModel
from typing import Optional

class SAKPC_LPU(BaseModel):
    COUNTER: Optional[int]
    LPUCODE: int
    NAME: Optional[str]

    class Config:
        from_attributes = True


class SAKPC_LPUDetail(BaseModel):
    LPUCODE: int
    NAME: Optional[str]
    NPOST: Optional[str] 
    FACE: Optional[str] 
    PHONE: Optional[int] 
    FAX: Optional[int] 
    FACE1: Optional[str] 
    PHONE1: Optional[int] 
    NPOST3: Optional[str] 
    FACE3: Optional[str] 
    E_MAIL3: Optional[str] 
    PHONE3: Optional[int]
    WWW: Optional[str] 

    class Config:
        from_attributes = True
