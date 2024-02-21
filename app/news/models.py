from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date

"""Модель сообщения"""
class News(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(default=date.today())


    def __str__(self):
        return f"({self.id}) {self.title}"