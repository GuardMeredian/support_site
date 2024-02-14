from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AttachmentSchema(BaseModel):
    id: Optional[int] = None
    file_name: str
    file_path: str
    ticket_id: int

    class Config:
        orm_mode = True