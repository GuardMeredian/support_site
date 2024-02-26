from typing import List, TypeVar
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload
from app.tikets.messages.schemas import SMessage
from app.tikets.models import Ticket
from app.database import async_session_maker
from app.DAO.base import BaseDAO
from app.tikets.schemas import SCreateTicket, STicketSummury, SUpdateTicket
from app.tikets.messages.models import Messages
from app.users.models import User

T = TypeVar('T')

class TicketDAO(BaseDAO[Ticket]):
    model = Ticket
    
        
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
            query = select(cls.model).options(joinedload(cls.model.messages).options(
                joinedload(Messages.creator)  # Загружаем данные автора сообщения
            ),
                                              joinedload(cls.model.attachments),
                                              joinedload(cls.model.creator),
                                              joinedload(cls.model.organization),
                                              joinedload(cls.model.assigned),
                                              joinedload(cls.model.status),
                                              joinedload(cls.model.system)
                                              ).where(cls.model.id == ticket_id)
            result = await session.execute(query)
            ticket = result.mappings().first()
            ticket_detail = ticket['Ticket']
            return ticket_detail
        
    @classmethod
    async def add_message(cls, ticket_id: int, message_data: SMessage) -> SMessage:
        async with async_session_maker() as session:
            # Получаем объект пользователя из базы данных по id
            creator = await session.get(User, message_data.creator.id)
            if not creator:
                raise ValueError(f"User with id {message_data.creator.id} not found")


            # Создаем новый объект сообщения
            new_message = Messages(
                content=message_data.content,
                creator=creator,  # Используем объект creator, полученный из сессии
                ticket_id=ticket_id,  # Связываем с тикетом по id
                created_at=message_data.created_at  # Устанавливаем время создания сообщения
            )
            session.add(new_message)
            await session.commit()

        # Возвращаем созданное сообщение
        return new_message

    @classmethod
    async def get_tickets_by_org(cls, organization_id: int) -> List[Ticket]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(organization_id=organization_id)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_all_summary(cls, **filter_by) -> List[STicketSummury]:
        async with async_session_maker() as session:
        # Используйте joinedload для загрузки связанных объектов
           query = select(cls.model).options(
                joinedload(cls.model.status),
                joinedload(cls.model.system),
                joinedload(cls.model.creator),
                joinedload(cls.model.organization),
                joinedload(cls.model.assigned)
            ).filter_by(**filter_by)
        result = await session.execute(query)
         # Извлекаем все строки из результата запроса
        tickets = result.scalars().all()
            # Преобразуем каждый объект Ticket в словарь, соответствующий схеме STicketSummury
        tickets_summary = [
                STicketSummury(
                    id=ticket.id,
                    title=ticket.title,
                    status=ticket.status,
                    system=ticket.system,
                    priority=ticket.priority,
                    creator=ticket.creator,
                    assigned=ticket.assigned,
                    created_at=ticket.created_at,
                    updated_at=ticket.updated_at,
                    organization=ticket.organization
                )
                for ticket in tickets
            ]
        return tickets_summary
        #return result.mappings().all()
        # 
    @staticmethod
    async def update_ticket_status(ticket_id: int, status_id: int):
        async with async_session_maker() as session:
            # Создаем запрос для выбора тикета с указанным ID
            stmt = select(Ticket).where(Ticket.id == ticket_id)
            # Загружаем связанные данные статуса
            stmt = stmt.options(selectinload(Ticket.status))
            # Выполняем запрос
            result = await session.execute(stmt)
            ticket = result.scalars().first()

            if not ticket:
                # Тикет не найден
                return None
            # Обновляем статус тикета
            ticket.status_id = status_id
            # Сохраняем изменения в базе данных
            await session.commit()
        return ticket    