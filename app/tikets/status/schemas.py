from pydantic import BaseModel
from typing import Optional

class SStatus(BaseModel):
    id: Optional[int] = None
    description: str

    class Config:
        from_attributes = True