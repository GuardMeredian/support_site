from typing import List, TypeVar
from sqlalchemy import select
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.news.models import News
from app.news.schemas import SNews

T = TypeVar('T')

class NewsDAO(BaseDAO[News]):
    model = News

    @classmethod
    async def create_news(cls, news_data: SNews) -> News:
        async with async_session_maker() as session:
            new_news = cls.model(**news_data.model_dump(exclude_unset=True))
            session.add(new_news)
            await session.flush()
            await session.commit()
            return new_news

    @classmethod
    async def get_news_list(cls) -> List[News]:
        async with async_session_maker() as session:
            messages = await session.execute(select(cls.model.__table__.columns))
            return messages.mappings().all()