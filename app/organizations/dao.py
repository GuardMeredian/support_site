
from typing import TypeVar
from sqlalchemy import select
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.organizations.models import Organization
from sqlalchemy.orm import joinedload

T = TypeVar('T')

class OrganizationDAO(BaseDAO[Organization]):
    model = Organization

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
            org = result.mappings().first()
            org_detail = org['Organization']
            return org_detail
        
    