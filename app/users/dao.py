from typing import Generic, TypeVar
from sqlalchemy import insert, select, update, delete
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User
from app.auth.auth import pwd_context

T = TypeVar('T')

class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def find_by_username(cls, username: str) -> User | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(login=username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_email(cls, email: str) -> User | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_organization(cls, organization_id: int) -> list[User]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(organization_id=organization_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_role(cls, role_id: int) -> list[User]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(role_id=role_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update_user_role(cls, user_id: int, role_id: int) -> User:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == user_id).values(role_id=role_id)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=user_id)

    @classmethod
    async def update_user_email(cls, user_id: int, email: str) -> User:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == user_id).values(email=email)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=user_id)

    @classmethod
    async def update_password(cls, user_id: int, hashed_password: str) -> User:
        async with async_session_maker() as session:
            # Получаем пользователя по ID
            user = await session.get(User, user_id)
            if user:
                # Обновляем пароль пользователя
                user.password = hashed_password
                # Обновляем пользователя в базе данных
                await session.commit()
                return user
            else:
                raise ValueError(f"User with ID {user_id} not found")
        