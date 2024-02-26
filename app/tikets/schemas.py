from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.tikets.attachments.schemas import SAttachment
from app.tikets.messages.schemas import SMessage
from app.users.schemas import SUserForTicket
from app.organizations.schemas import SOrgForTicket
from app.tikets.status.schemas import SStatus
from app.tikets.system.schemas import SSystem

class SDetailTicket(BaseModel):
    id: int
    title: str
    description: str
    status: SStatus
    system: SSystem
    priority: Optional[int] = None
    creator: SUserForTicket
    assigned: Optional[SUserForTicket] = None
    created_at: date
    updated_at: Optional[date] = None
    organization: SOrgForTicket
    messages: List[SMessage] = []
    attachments: List[SAttachment] = []

    class Config:
        from_attributes = True

class STicketSummury(BaseModel):
    id: int 
    title: str
    status: SStatus
    system: SSystem
    priority: Optional[int] = None
    creator: SUserForTicket
    assigned: Optional[SUserForTicket] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    organization: SOrgForTicket

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
    attachments: List[SAttachment] = []

    class Config:
        from_attributes=True


class SUpdateTicket(BaseModel):
    title: str
    description: str
    

    class Config:
        from_attributes = True


class SUpdateTicketStatus(BaseModel):
    status_id: int

    class Config:
        from_attributes = True