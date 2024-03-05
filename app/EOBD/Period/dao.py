from datetime import datetime
from typing import List, TypeVar
from sqlalchemy import  select
from app.DAO.base import BaseDAO
from app.database import eobd_async_session
from app.EOBD.Period.models import Period

T = TypeVar('T')

class PeriodDAO(BaseDAO[Period]): 
    model = Period

    @classmethod
    async def get_period_list(cls) -> List[Period]:
        # Определение текущего года
        current_year = datetime.now().year
        previous_year = current_year - 1

        async with eobd_async_session() as session:
            # Создание запроса с условием фильтрации по году и группировкой по LPUCODE
            current_year_query = (
                select(cls.model)
                .where(cls.model.YEAR == current_year)
            )
            previous_year_query = (
                select(cls.model)
                .where(cls.model.YEAR == previous_year)
            )

            # Выполнение запроса за текущий год
            current_year_messages = await session.execute(current_year_query)
            current_year_periods = current_year_messages.scalars().all()

            # Если данных за текущий год нет, выполняем запрос за предыдущий год
            if not current_year_periods:
                previous_year_messages = await session.execute(previous_year_query)
                return previous_year_messages.scalars().all()

            return current_year_periods