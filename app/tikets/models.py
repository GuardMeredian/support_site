from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import ForeignKey
from datetime import datetime
from app.status.models import Status


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey('status.id'), nullable=False)
    priority: Mapped[int] = mapped_column(default=1)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    assigned_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'), nullable=False)  # Добавлен внешний ключ
    organization = relationship("Organization", back_populates="tickets")  # Отношение к Organization
    # ... другие поля и отношения ...

    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_tickets")
    assigned = relationship("User", foreign_keys=[assigned_id], back_populates="assigned_tickets")
    status = relationship("Status", back_populates="tickets")