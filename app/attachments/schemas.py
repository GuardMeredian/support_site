from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SAttachment(BaseModel):
    id: int
    ticket_id: int
    filename: str
    file_path: str
    #message_id: Optional[int] = None

    class Config:
        orm_mode = True