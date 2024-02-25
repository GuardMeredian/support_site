
import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from app.tikets.attachments.models import Attachments
from app.exceptions import MessageIsNotAddException, TicketIsNotAddException, TicketIsNotFoundException, TicketIsNotUpdateException, UserNotAuthException
from app.tikets.messages.schemas import SMessage
from app.tikets.dao import TicketDAO
from app.tikets.models import Ticket
from app.tikets.schemas import STicketSummury, SDetailTicket, SCreateTicket, SUpdateTicket
from typing import Annotated, Dict, List
from app.database import async_session_maker
from app.users.dependescies import get_current_user
from app.users.models import User


router = APIRouter(
    prefix="/tickets",
    tags=["Заявки"])


@router.get("/all_tickets", response_model=List[STicketSummury])
async def get_all_tickets(current_user: dict = Depends(get_current_user)) -> List[Ticket]:
    user = current_user["User"]
    if user.role_id == 3:
        tickets = await TicketDAO.find_all_summary(organization_id=user.organization_id)
    else:    
        tickets = await TicketDAO.find_all_summary()
    return tickets

@router.get("/{ticket_id}", response_model=SDetailTicket)
async def get_detail_ticket(ticket_id: int) -> Ticket:
    ticket = await TicketDAO.get_ticket_with_messages(ticket_id)
    if not ticket:
        raise TicketIsNotFoundException
    return ticket

@router.put("/{ticket_id}", response_model=SUpdateTicket)
async def update_ticket(ticket_id: int, ticket_data: Annotated[SUpdateTicket, Depends()], current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException
    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise TicketIsNotFoundException

    # Обновляем тикет в базе данных
    updated_ticket = await TicketDAO.update_ticket(ticket_id, ticket_data)
    if not updated_ticket:
        raise TicketIsNotUpdateException

    return updated_ticket

@router.post("/add_ticket", response_model=SCreateTicket)
async def create_ticket(ticket_data: Annotated[SCreateTicket, Depends()], current_user: dict = Depends(get_current_user)):
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

@router.post("/upload_file/{ticket_id}", response_model=Dict[str, str])
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


@router.post("/{ticket_id}/add_message", response_model=SMessage)
async def add_message_to_ticket(ticket_id: int, message_data:Annotated[SMessage, Depends()], current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException
    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise TicketIsNotFoundException
    
    # Добавляем сообщение в базу данных
    new_message = await TicketDAO.add_message(ticket_id, message_data)
    if not new_message:
        raise MessageIsNotAddException

    return new_message