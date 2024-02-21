from pydantic import BaseModel
from typing import Optional

class SSystem(BaseModel):
    id: Optional[int] = None
    description: str

    class Config:
        from_attributes = True