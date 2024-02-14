from typing import Generic, Optional, TypeVar
from sqlalchemy import insert, select, update, delete
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.roles.models import Roles

T = TypeVar('T')

class RoleDAO(BaseDAO[Roles]):
    model = Roles

    # Создание новой роли
    @classmethod
    async def create(cls, **values) -> Roles:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**values)
            result = await session.execute(stmt)
            return result.scalar_one()

    # Получение роли по ID
    @classmethod
    async def get(cls, id: int) -> Optional[Roles]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Обновление существующей роли
    @classmethod
    async def update(cls, id: int, **values) -> Roles:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == id).values(**values)
            await session.execute(stmt)
            await session.commit()
            return await cls.get(id)

    # Удаление роли по ID
    @classmethod
    async def delete(cls, id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id)
            await session.execute(stmt)
            await session.commit()

    # Получение всех ролей
    @classmethod
    async def get_all(cls) -> list[Roles]:
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    # ... (дополнительные методы RoleDAO, если они нужны)