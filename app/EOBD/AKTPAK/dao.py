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
                (cls.model.D_FIN.isnot(None)) & 
                (cls.model.NAME_S.isnot(None))
            ).order_by(cls.model.LPUCODE)
            result = await session.execute(query)
            lpus = result.scalars().all()
        return lpus