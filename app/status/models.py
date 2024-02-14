from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Status(Base):
   __tablename__ = "status"

   id: Mapped[int] = mapped_column(primary_key=True)
   description: Mapped[str]
   tickets = relationship("Ticket", back_populates="status")


   def __str__(self):
        return f"{self.description} ({self.id})"