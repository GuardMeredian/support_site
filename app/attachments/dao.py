from typing import Generic, Optional, TypeVar
from sqlalchemy import insert, select, update, delete
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.attachments.models import Attachments

T = TypeVar('T')

class AttachmentDAO(BaseDAO[Attachments]):
    model = Attachments

    # Создание нового вложения
    @classmethod
    async def create(cls, **values) -> Attachments:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**values)
            result = await session.execute(stmt)
            return result.scalar_one()

    # Получение вложения по ID
    @classmethod
    async def get(cls, id: int) -> Optional[Attachments]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Обновление существующего вложения
    @classmethod
    async def update(cls, id: int, **values) -> Attachments:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == id).values(**values)
            await session.execute(stmt)
            await session.commit()
            return await cls.get(id)

    # Удаление вложения по ID
    @classmethod
    async def delete(cls, id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id)
            await session.execute(stmt)
            await session.commit()

    # Получение всех вложений для определенного тикета
    @classmethod
    async def find_by_ticket_id(cls, ticket_id: int) -> list[Attachments]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(ticket_id=ticket_id)
            result = await session.execute(query)
            return result.scalars().all()

    # ... (дополнительные методы AttachmentDAO, если они нужны)