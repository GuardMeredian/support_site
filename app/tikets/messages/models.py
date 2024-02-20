from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import date

"""Модель сообщения"""
class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('tickets.id'), nullable=False)
    created_at: Mapped[date] = mapped_column(default=date.today())
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_messages")
    ticket = relationship("Ticket", foreign_keys=[ticket_id], back_populates="messages", lazy='select')

    def __str__(self):
        return f"({self.id}) {self.content}"


