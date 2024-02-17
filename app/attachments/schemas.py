from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SAttachment(BaseModel):
    id: Optional[int]
    ticket_id: Optional[int]
    filename: Optional[str]
    file_url: str
    #message_id: Optional[int] = None

    class Config:
        orm_mode = True