import os
import shutil
from typing import Annotated, Generic, List, Optional, TypeVar
from fastapi import Depends, File, UploadFile
from sqlalchemy import select, join, update
from sqlalchemy.orm import joinedload
from app.attachments.models import Attachments
from app.messages.schemas import SMessage
from app.tikets.models import Ticket
from app.database import async_session_maker
from app.DAO.base import BaseDAO
from app.tikets.schemas import SCreateTicket, SUpdateTicket
from app.messages.models import Messages

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
    async def get_all_tickets(cls, **filter_by) -> list[Ticket]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(**filter_by)
            result = await session.execute(query)
            tickets = result.mappings().all()
            return tickets
        
    @classmethod
    async def update_ticket(cls, ticket_id: int, ticket_data: SUpdateTicket) -> Ticket:
        async with async_session_maker() as session:
        # Преобразование данных тикета в словарь для обновления, исключая неустановленные поля
            ticket_data_dict = ticket_data.model_dump(exclude_unset=True)
        # Удаление ключа 'id', так как он не должен быть обновлен
        # Обновление данных тикета
            stmt = update(cls.model).where(cls.model.id == ticket_id).values(**ticket_data_dict)
            await session.execute(stmt)
            await session.commit()
        # Возвращение обновленного тикета
            return await cls.find_one_or_none(id=ticket_id)

    @classmethod
    async def create_ticket(cls, ticket_data: SCreateTicket) -> Ticket:
        async with async_session_maker() as session:
            # Преобразование данных тикета в словарь для вставки, исключая неустановленные поля
            ticket_data_dict = ticket_data.model_dump(exclude_unset=True)
            new_ticket = cls.model(**ticket_data_dict)
            session.add(new_ticket)
            await session.flush()  # Сначала добавляем тикет, чтобы получить его ID
            await session.commit()
            return new_ticket
            #return new_ticket

    @classmethod
    async def get_ticket_with_messages(cls, ticket_id: int) -> Ticket:
        async with async_session_maker() as session:
            # Используем joinedload для оптимизации запроса
            query = select(cls.model).options(joinedload(cls.model.messages),
                                              joinedload(cls.model.attachments),
                                              joinedload(cls.model.creator),
                                              joinedload(cls.model.organization),
                                              joinedload(cls.model.assigned)
                                              ).where(cls.model.id == ticket_id)
            result = await session.execute(query)
            ticket = result.mappings().first()
            ticket_detail = ticket['Ticket']
            return ticket_detail
        
    @classmethod
    async def add_message(cls, ticket_id: int, message_data: SMessage) -> SMessage:
        async with async_session_maker() as session:
            # Создаем новый объект сообщения
            new_message = Messages(
                content=message_data.content,
                creator_id=message_data.creator_id,
                ticket_id=ticket_id  # Связываем с тикетом по id
            )
            session.add(new_message)
            await session.commit()

        # Возвращаем созданное сообщение
        return new_message    