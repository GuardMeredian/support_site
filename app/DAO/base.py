from typing import Generic, TypeVar, Optional
from sqlalchemy import insert, select, update, delete
from app.database import async_session_maker


T = TypeVar('T')

class BaseDAO(Generic[T]):
    model: T = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[T]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().first()


    @classmethod
    async def find_all(cls, **filter_by) -> list[T]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create(cls, **values) -> T:
        async with async_session_maker() as session:
            stmt = insert(cls.model.__table__.columns).values(**values)
            result = await session.execute(stmt)
            return result.mapings().one()

    @classmethod
    async def update(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(**filter_by)
            await session.execute(stmt)

    @classmethod
    async def delete(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(**filter_by)
            await session.execute(stmt)