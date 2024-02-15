from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import date
#from app.attachments.models import Attachments

class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('tickets.id'), nullable=False)
    created_at: Mapped[date] = mapped_column(default=date.today())
    #updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    #assigned_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_messages")
    ticket = relationship("Ticket", foreign_keys=[ticket_id], back_populates="messages", lazy='select')
    #assigned = relationship("User", foreign_keys=[assigned_id], back_populates="assigned_messages")
    # Добавьте эту строку в модель Messages в файле messages/models.py
    #attachments = relationship("Attachments", back_populates="message")

    def __str__(self):
        return f"({self.id}) {self.content}"


