from datetime import datetime
from typing import Generic, TypeVar
from sqlalchemy import insert, select, update, delete
from app.DAO.base import BaseDAO
from app.users.models import User
from app.database import async_session_maker
from app.organizations.models import Organization
from sqlalchemy.orm import joinedload

T = TypeVar('T')

class OrganizationDAO(BaseDAO[Organization]):
    model = Organization

    @classmethod
    async def find_by_name(cls, name: str) -> Organization | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(name=name)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_contact_info(cls, contact_info: str) -> Organization | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(contact_info=contact_info)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_user(cls, user_id: int) -> list[Organization]:
        async with async_session_maker() as session:
            query = select(cls.model).join(User).filter(User.id == user_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update_organization_name(cls, organization_id: int, new_name: str) -> Organization:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == organization_id).values(name=new_name)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=organization_id)

    @classmethod
    async def create_organization(cls, **values) -> Organization:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**values)
            result = await session.execute(stmt)
            return result.scalar_one()

    @classmethod
    async def delete_organization(cls, organization_id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == organization_id)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update_organization_contact_info(cls, organization_id: int, new_contact_info: str) -> Organization:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == organization_id).values(contact_info=new_contact_info)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=organization_id)

    @classmethod
    async def add_user_to_organization(cls, organization_id: int, user_id: int) -> None:
        # Здесь должен быть код для добавления пользователя в организацию
        pass

    @classmethod
    async def remove_user_from_organization(cls, organization_id: int, user_id: int) -> None:
        # Здесь должен быть код для удаления пользователя из организации
        pass

    @classmethod
    async def find_organizations_by_role(cls, role_id: int) -> list[Organization]:
        # Здесь должен быть код для поиска организаций по роли пользователя
        pass

    @classmethod
    async def find_organizations_by_status(cls, status: str) -> list[Organization]:
        # Здесь должен быть код для поиска организаций по статусу
        pass

    @classmethod
    async def count_organizations(cls) -> int:
        async with async_session_maker() as session:
            return await session.query(cls.model).count()

    @classmethod
    async def find_organizations_by_creation_date(cls, start_date: datetime, end_date: datetime) -> list[Organization]:
        # Здесь должен быть код для поиска организаций по дате создания
        pass

    @classmethod
    async def get_orgs(cls, **filter_by) -> list[Organization]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(**filter_by).order_by(cls.model.lpucode)
            result = await session.execute(query)
            tickets = result.mappings().all()
            return tickets
        
    @classmethod
    async def get_org_card(cls, organization_id: int) -> Organization:
        async with async_session_maker() as session:
            # Используем joinedload для оптимизации запроса
            query = select(cls.model).options(joinedload(cls.model.users)).where(cls.model.id == organization_id)
            result = await session.execute(query)
            ticket = result.mappings().first()
            ticket_detail = ticket['Organization']
            return ticket_detail
        
    