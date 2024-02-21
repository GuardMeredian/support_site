from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

"""Модель статуса"""
class System(Base):
   __tablename__ = "systems"

   id: Mapped[int] = mapped_column(primary_key=True)
   description: Mapped[str]
   tickets = relationship("Ticket", back_populates="system")


   def __str__(self):
        return f"{self.description} ({self.id})"