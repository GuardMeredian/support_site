from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.attachments.schemas import AttachmentSchema
from app.messages.schemas import SMessage

class SDetailTicket(BaseModel):
    id: int 
    title: str
    description: str
    status_id: int
    priority: Optional[int] =   None
    creator_id: int
    assigned_id: Optional[int] = None
    created_at:date 
    updated_at: Optional[date] = None
    organization_id: int
    messages: Optional[List['SMessage']] = []
    #attachments: Optional[List['AttachmentSchema']] = []

    class Config:
        from_attributes = True

class STicketSummury(BaseModel):
    id: int 
    title: str
    status_id: int
    priority: Optional[int] = None
    creator_id: int
    assigned_id: Optional[int] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    organization_id: int

    class Config:
        from_attributes=True

class SCreateTicket(BaseModel):
    title: str
    description: str
    status_id: int
    priority: Optional[int] = None
    creator_id: int
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    organization_id: int

    class Config:
        from_attributes=True

