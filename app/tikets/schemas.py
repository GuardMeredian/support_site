from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.attachments.schemas import AttachmentSchema
from app.messages.schemas import MessageSchema

class TicketSchema(BaseModel):
    id: int 
    title: str
    description: str
    status_id: int
    priority: Optional[int] =   1
    creator_id: int
    assigned_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    messages: Optional[List['MessageSchema']] = []
    attachments: Optional[List['AttachmentSchema']] = []

    class Config:
        orm_mode = True



