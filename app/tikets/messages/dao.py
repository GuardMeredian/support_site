from typing import List, TypeVar
from sqlalchemy import select
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.tikets.messages.models import Messages
from app.tikets.messages.schemas import SMessage

T = TypeVar('T')

class MessageDAO(BaseDAO[Messages]):
    model = Messages

    @classmethod
    async def create_message(cls, message_data: SMessage) -> Messages:
        async with async_session_maker() as session:
            new_message = cls.model(**message_data.model_dump(exclude_unset=True))
            session.add(new_message)
            await session.flush()
            await session.commit()
            return new_message

    @classmethod
    async def get_messages_for_ticket(cls, ticket_id: int) -> List[Messages]:
        async with async_session_maker() as session:
            messages = await session.execute(select(cls.model.__table__.columns).where(cls.model.ticket_id == ticket_id))
            return messages.mappings().all()