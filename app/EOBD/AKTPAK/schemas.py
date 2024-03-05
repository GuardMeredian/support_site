from pydantic import BaseModel
from typing import Optional

class SAKPC_LPU(BaseModel):
    COUNTER: Optional[int]
    LPUCODE: int
    NAME_S: Optional[str]

    class Config:
        from_attributes = True
