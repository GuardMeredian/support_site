
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.tikets.attachments.models import Attachments
from app.exceptions import MessageIsNotAddException, TicketIsNotAddException, TicketIsNotFoundException, TicketIsNotUpdateException, UserNotAuthException
from app.tikets.messages.schemas import SMessage
from app.tikets.dao import TicketDAO
from app.tikets.models import Ticket
from app.tikets.schemas import STicketSummury, SDetailTicket, SCreateTicket, SUpdateTicketControlDate, SUpdateTicketOperator, SUpdateTicketStatus
from typing import Annotated, Dict, List, Optional
from app.database import async_session_maker
from app.users.dependescies import get_current_user
from app.users.models import User

from datetime import date


router = APIRouter(
    prefix="/tickets",
    tags=["Заявки"])


@router.get("/all_tickets", response_model=List[STicketSummury], name="Получить все заявки", description="Получить список всех заявок")
async def get_all_tickets(current_user: dict = Depends(get_current_user),
                      system: Optional[int] = None,
                      status: Optional[int] = None,
                      organization: Optional[int] = None,
                      assigned: Optional[int] = None,
                      ticket_id: Optional[int] = None) -> List[Ticket]:
    user = current_user['User']
    if user['role']['id'] == 2:
        organization_id = user['organization']['id']
        tickets = await TicketDAO.find_all_summary(organization_id=organization_id)
    else:    
        if not any([ticket_id, system, status, organization, assigned]):
            tickets = await TicketDAO.find_all_summary()
        else:
            tickets = await TicketDAO.find_all_summary(system=system,
                                             status=status,
                                             organization=organization,
                                             assigned=assigned,
                                             ticket_id=ticket_id)
    return tickets

@router.get("/{ticket_id}", response_model=SDetailTicket, name="Получить детали заявки", description="Получить детальную информацию о заявке по ID")
async def get_detail_ticket(ticket_id: int) -> Ticket:
    ticket = await TicketDAO.get_ticket_with_messages(ticket_id)
    if not ticket:
        raise TicketIsNotFoundException
    return ticket


@router.post("/add_ticket", response_model=SCreateTicket , name="Создать заявку", description="Создать новую заявку")
async def create_ticket(ticket_data: SCreateTicket, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException
        # Создаем новый тикет в базе данных
    try:
        new_ticket = await TicketDAO.create_ticket(ticket_data)
    except:
        raise TicketIsNotAddException

    if not new_ticket:
        raise TicketIsNotAddException

    return new_ticket

@router.post("/upload_file/{ticket_id}", response_model=Dict[str, str], name="Загрузить файл", description="Загрузить файл к заявке")
async def upload_file(ticket_id: int, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException
    # Проверяем, существует ли директория static/files
    static_files_dir = os.path.join(os.getcwd(), 'static', 'files')
    if not os.path.exists(static_files_dir):
        os.makedirs(static_files_dir)

    # Сохраняем файл в директорию static/files
    file_path = os.path.join(static_files_dir, file.filename)
    with open(file_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # Формируем ссылку на файл
    file_url = f'/static/files/{file.filename}'

    # Сохраняем данные о файле в базе данных
    async with async_session_maker() as session:
        attachment = Attachments(
            filename=file.filename,
            file_url=file_url,
            ticket_id=ticket_id  # Связываем с тикетом по id
        )
        session.add(attachment)
        await session.commit()

    # Возвращаем JSON с именем файла и ссылкой на файл
    return JSONResponse(content={
        "msg": "фаил загружен"
    })


@router.post("/{ticket_id}/add_message", response_model=SMessage, name="Добавить сообщение", description="Добавить сообщение к заявке")
async def add_message_to_ticket(ticket_id: int, message_data: SMessage, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException
    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise TicketIsNotFoundException
    
    # Проверяем, что сообщение содержит необходимые данные
    if not message_data.content or not message_data.creator or not message_data.creator.id:
        raise HTTPException(status_code=400, detail="Message content or creator data is missing")
    
    # Добавляем сообщение в базу данных
    new_message = await TicketDAO.add_message(ticket_id, message_data)
    if not new_message:
        raise MessageIsNotAddException

    return new_message

@router.put("/{ticket_id}/status", response_model=SUpdateTicketStatus, name="Обновить статус заявки", description="Обновить статус заявки")
async def update_ticket_status(ticket_id: int, status_data: SUpdateTicketStatus, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException

    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise TicketIsNotFoundException

    # Обновляем статус тикета в базе данных
    updated_ticket = await TicketDAO.update_ticket_status(ticket_id, status_data.status_id)
    if not updated_ticket:
        raise TicketIsNotFoundException

    return updated_ticket

@router.put("/{ticket_id}/operator", response_model=SUpdateTicketOperator, name="Обновить оператора", description="Обновить оператора, ответственного за заявку")
async def update_ticket_operator(ticket_id: int, user_data: SUpdateTicketOperator, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException

    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise TicketIsNotFoundException

    # Обновляем статус тикета в базе данных
    updated_ticket = await TicketDAO.update_ticket_operator(ticket_id, user_data.assigned_id)
    if not updated_ticket:
        raise TicketIsNotFoundException

    return updated_ticket


@router.put("/{ticket_id}/control_date", response_model=SUpdateTicketControlDate, name="Обновить дату контроля", description="Обновить дату контроля заявки")
async def update_ticket_control_date(ticket_id: int, user_data: SUpdateTicketControlDate, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException

    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise TicketIsNotFoundException

    # Обновляем статус тикета в базе данных
    updated_ticket = await TicketDAO.update_ticket_control_date(ticket_id, user_data.control_date)
    if not updated_ticket:
        raise TicketIsNotFoundException

    return updated_ticket