from typing import Optional
from sqlalchemy import JSON, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Attachments(Base):
    __tablename__ = 'attachments'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str]= mapped_column(nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('tickets.id'))
    #message_id: Mapped[int] = mapped_column(ForeignKey('messages.id'))

    ticket = relationship("Ticket", back_populates="attachments")
    #message = relationship("Message", back_populates="attachments")