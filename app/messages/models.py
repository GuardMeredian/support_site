from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime
from app.attachments.models import Attachments

class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    assigned_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_messages")
    assigned = relationship("User", foreign_keys=[assigned_id], back_populates="assigned_messages")
    # Добавьте эту строку в модель Messages в файле messages/models.py
    attachments = relationship("Attachments", back_populates="message")
