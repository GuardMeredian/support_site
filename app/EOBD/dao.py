from typing import List, Dict, Any, TypeVar, Optional
from sqlalchemy import text
from app.DAO.base import BaseDAO
from app.database import TEST_async_session, TEMP_async_session

T = TypeVar('T')

class EobddDAO(BaseDAO):

    @staticmethod
    async def get_protocol(chief: int, year: int, year_qr: int) -> Dict[str, Any]:
        # Выбираем сессию в зависимости от статуса

        async with TEMP_async_session() as session:
            # Первый запрос для получения данных о посещениях
            visit_query = text(f"SET NOCOUNT ON; SELECT * FROM EOBD_TEMP.dbo.info_talon_39 WHERE chief = :chief AND year = :year AND year_qr = :year_qr")
            visit_result = await session.execute(visit_query, {"chief": chief, "year": year, "year_qr": year_qr})
            visit_rows = visit_result.fetchall()
            visit_data = [{key: value for key, value in zip(visit_result.keys(), row)} for row in visit_rows]

            # Второй запрос для получения данных из другой таблицы
            data_query = text(f"SET NOCOUNT ON; SELECT [type], [cnt], [v1], [v2], [sum], [date1], [date2] FROM EOBD_TEMP.dbo.info_talon WHERE chief = :chief AND year = :year AND year_qr = :year_qr ORDER BY counter")
            data_result = await session.execute(data_query, {"chief": chief, "year": year, "year_qr": year_qr})
            data_rows = data_result.fetchall()
            data = [{key: value for key, value in zip(data_result.keys(), row)} for row in data_rows]

            # Объединяем результаты в один словарь
            combined_data = {
                "data": data,
                "Visit": visit_data
            }

            return combined_data
