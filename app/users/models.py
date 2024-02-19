
from typing import Optional
from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, attributes
from app.database import Base
from app.roles.models import Roles
from app.organizations.models import Organization
from app.messages.models import Messages
from app.tikets.models import Ticket
from app.auth.auth import get_password_hash


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

    created_messages = relationship("Messages", foreign_keys=[Messages.creator_id], back_populates="creator", cascade="all, delete-orphan")
    #assigned_messages = relationship("Messages", foreign_keys=[Messages.assigned_id], back_populates="assigned")
    created_tickets = relationship("Ticket", foreign_keys=[Ticket.creator_id], back_populates="creator", cascade="all, delete-orphan")
    assigned_tickets = relationship("Ticket", foreign_keys=[Ticket.assigned_id], back_populates="assigned", cascade="all, delete-orphan")

    

    def hash_password(mapper, connection, target):
        if target.password: 
            target.password = get_password_hash(target.password)



    def __str__(self):
        return f"{self.surname} {self.name} {self.secname}({self.id})"
    
# Подписываемся на события before_insert и before_update для модели User
event.listen(User, 'before_insert', User.hash_password)
#event.listen(User, 'before_update', User.hash_password)
@event.listens_for(User, 'before_update')
def receive_before_update(mapper, connection, target):
    # Проверяем, было ли изменено поле password
    password_history = attributes.get_history(target, 'password')
    if password_history.added:
        # Обновляем пароль, если он был изменен
        target.password = get_password_hash(password_history.added[0])
    elif password_history.deleted:
        # Если пароль был удален, устанавливаем его в None
        target.password = None