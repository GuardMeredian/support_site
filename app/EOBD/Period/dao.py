from typing import List, TypeVar
from sqlalchemy import select
from app.DAO.base import BaseDAO
from app.database import eobd_async_session
from app.EOBD.Period.models import Period

T = TypeVar('T')

class PeriodDAO(BaseDAO[Period]): 
    model = Period

    @classmethod
    async def get_period_list(cls) -> List[Period]:
        async with eobd_async_session() as session:
            messages = await session.execute(select(cls.model.__table__.columns))
            return messages.mappings().all()