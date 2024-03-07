from typing import TypeVar
from sqlalchemy import select
from app.DAO.base import BaseDAO
from app.database import AKTPAK_async_session
from app.EOBD.AKTPAK.models import AKPC_LPU
from sqlalchemy.orm import joinedload

T = TypeVar('T')

class LPUDAO(BaseDAO[AKPC_LPU]):
    model = AKPC_LPU

    @classmethod
    async def get_orgs(cls) -> list[AKPC_LPU]:
        async with AKTPAK_async_session() as session:
            query = select(cls.model).where(
                (cls.model.D_FIN.is_(None)) & 
                (cls.model.NAME_S.isnot(None)) &
                (cls.model.TYPE_S == 2)
            ).order_by(cls.model.LPUCODE)
            result = await session.execute(query)
            lpus = result.scalars().all()
        return lpus
    

    @classmethod
    async def get_org_card(cls, organzation_id: int):
        async with AKTPAK_async_session() as session:
            query = select(cls.model).where(cls.model.COUNTER == organzation_id)
            result = await session.execute(query)
            org = result.scalars().first()
        return org