from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageSchema(BaseModel):
    id: Optional[int] = None
    content: str
    creator_id: int
    assigned_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True