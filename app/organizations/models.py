from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.tikets.models import Ticket

class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    lpucode: Mapped[int]
    name: Mapped[str]

    tickets = relationship("Ticket", back_populates="organization")
    users = relationship("User", back_populates="organization")

    def __str__(self):
        return f"({self.lpucode}){self.name}"