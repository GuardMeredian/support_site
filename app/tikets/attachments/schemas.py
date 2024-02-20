from pydantic import BaseModel
from typing import Optional

class SAttachment(BaseModel):
    id: Optional[int]
    ticket_id: Optional[int]
    filename: Optional[str]
    file_url: str
    

    class Config:
        from_attributes = True