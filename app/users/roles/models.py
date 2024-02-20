from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

"""Модель ролей"""
class Roles(Base):
   __tablename__ = "roles"

   id: Mapped[int] = mapped_column(primary_key=True)
   description: Mapped[str]
   users = relationship("User", back_populates="role")

   def __str__(self):
        return f"{self.description} ({self.id})"