from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Attachments(Base):
    __tablename__ = 'attachments'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    message_id: Mapped[int] = mapped_column(ForeignKey('messages.id'), nullable=False)


    message = relationship("Messages", back_populates="attachments")