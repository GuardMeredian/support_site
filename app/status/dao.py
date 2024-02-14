from typing import Generic, Optional, TypeVar
from sqlalchemy import insert, select, update, delete
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.status.models import Status

T = TypeVar('T')

class StatusDAO(BaseDAO[Status]):
    model = Status

    # Создание нового статуса
    @classmethod
    async def create(cls, **values) -> Status:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**values)
            result = await session.execute(stmt)
            return result.scalar_one()

    # Получение статуса по ID
    @classmethod
    async def get(cls, id: int) -> Optional[Status]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Обновление существующего статуса
    @classmethod
    async def update(cls, id: int, **values) -> Status:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == id).values(**values)
            await session.execute(stmt)
            await session.commit()
            return await cls.get(id)

    # Удаление статуса по ID
    @classmethod
    async def delete(cls, id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id)
            await session.execute(stmt)
            await session.commit()

    # Получение всех статусов
    @classmethod
    async def get_all(cls) -> list[Status]:
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    # ... (дополнительные методы StatusDAO, если они нужны)