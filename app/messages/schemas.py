from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SMessage(BaseModel):
    id: Optional[int] = None
    content: str
    ticket_id: int
    creator_id: int
    
    #assigned_id: Optional[int] = None
    created_at: Optional[datetime] = None
    #updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True