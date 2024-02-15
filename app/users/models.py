
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.roles.models import Roles
from app.organizations.models import Organization
from app.messages.models import Messages
from app.tikets.models import Ticket
from app.auth.auth import pwd_context


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    secname: Mapped[str] = mapped_column(nullable=False)
    post: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))

    contact_tel: Mapped[str] = mapped_column(nullable=True)

    organization = relationship("Organization", back_populates="users")

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role = relationship("Roles", back_populates="users")

    created_messages = relationship("Messages", foreign_keys=[Messages.creator_id], back_populates="creator")
    #assigned_messages = relationship("Messages", foreign_keys=[Messages.assigned_id], back_populates="assigned")
    created_tickets = relationship("Ticket", foreign_keys=[Ticket.creator_id], back_populates="creator")
    assigned_tickets = relationship("Ticket", foreign_keys=[Ticket.assigned_id], back_populates="assigned")

    def set_password(self, raw_password):

        self.password = pwd_context.hash(raw_password)
        
        
        


    def __str__(self):
        return f"{self.surname} {self.name} {self.secname} ({self.id})"