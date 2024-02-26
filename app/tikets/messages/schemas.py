from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.users.schemas import SUserForMsg


class SMessage(BaseModel):
    #id: Optional[int] = None
    content: str
    ticket_id: int
    creator: SUserForMsg
    
    #assigned_id: Optional[int] = None
    created_at: Optional[datetime] = None
    #updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


    