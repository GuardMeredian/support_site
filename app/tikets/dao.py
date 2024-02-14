from typing import Generic, TypeVar
from sqlalchemy import insert, select, update
from app.tikets.models import Ticket
from app.database import async_session_maker
from app.DAO.base import BaseDAO
from app.tikets.schemas import TicketSchema

T = TypeVar('T')

class TicketDAO(BaseDAO[Ticket]):
    model = Ticket
    
    @classmethod
    async def find_by_status(cls, status_id: int) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select([column for column in cls.model.__table__.columns]).filter_by(status_id=status_id)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_by_priority(cls, priority: int) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select([column for column in cls.model.__table__.columns]).filter_by(priority=priority)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_by_creator(cls, creator_id: int) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select([column for column in cls.model.__table__.columns]).filter_by(creator_id=creator_id)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_by_assignee(cls, assigned_id: int) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select([column for column in cls.model.__table__.columns]).filter_by(assigned_id=assigned_id)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_open_tickets(cls) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select([column for column in cls.model.__table__.columns]).filter_by(status_id=1)  # Assuming   1 is the ID for open status
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_closed_tickets(cls) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select([column for column in cls.model.__table__.columns]).filter_by(status_id=2)  # Assuming   2 is the ID for closed status
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def assign_ticket(cls, ticket_id: int, assignee_id: int) -> Ticket:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == ticket_id).values(assigned_id=assignee_id)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=ticket_id)

    @classmethod
    async def change_ticket_status(cls, ticket_id: int, status_id: int) -> Ticket:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == ticket_id).values(status_id=status_id)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=ticket_id)

    @classmethod
    async def update_ticket_priority(cls, ticket_id: int, priority: int) -> Ticket:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == ticket_id).values(priority=priority)
            await session.execute(stmt)
            await session.commit()
            return await cls.find_one_or_none(id=ticket_id)
    
    @classmethod
    async def get_all_tickets(cls, **filter_by) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(**filter_by)
            result = await session.execute(query)
            tickets = result.mappings().all()
            return tickets
        
    @classmethod
    async def update_ticket(cls, ticket_id: int, ticket_data: TicketSchema) -> Ticket:
        async with async_session_maker() as session:
        # Преобразование данных тикета в словарь для обновления, исключая неустановленные поля
            ticket_data_dict = ticket_data.model_dump(exclude_unset=True)
        # Удаление ключа 'id', так как он не должен быть обновлен
            ticket_data_dict.pop('id', None)
            ticket_data_dict.pop('messages', None)
            ticket_data_dict.pop('attachments', None)
        # Обновление данных тикета
            stmt = update(cls.model).where(cls.model.id == ticket_id).values(**ticket_data_dict)
            await session.execute(stmt)
            await session.commit()
        # Возвращение обновленного тикета
            return await cls.find_one_or_none(id=ticket_id)

    @classmethod
    async def create_ticket(cls, ticket_data: TicketSchema) -> Ticket:
        async with async_session_maker() as session:
            # Преобразование данных тикета в словарь для вставки, исключая неустановленные поля
            ticket_data_dict = ticket_data.dict(exclude_unset=True)
            # Удаление ключей отношений, так как они не должны быть вставлены напрямую
            ticket_data_dict.pop('messages', None)
            ticket_data_dict.pop('attachments', None)
            # Создаем новый тикет
            stmt = insert(cls.model).values(**ticket_data.model_dump(exclude_unset=True))
            result = await session.execute(stmt)
            new_ticket = result.mappings().one()
            await session.commit()
            return new_ticket