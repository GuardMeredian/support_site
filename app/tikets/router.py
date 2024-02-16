from fastapi import APIRouter, HTTPException, UploadFile, File
from app.attachments.schemas import SAttachment
from app.tikets.dao import TicketDAO
from app.tikets.models import Ticket
from app.tikets.schemas import STicketSummury, SDetailTicket, SCreateTicket
from typing import List, Optional


router = APIRouter(
    prefix="/tickets",
    tags=["Заявки"])


@router.get("/all_tickets", response_model=List[STicketSummury])
async def get_all_tickets():
    tickets = await TicketDAO.get_all_tickets()
    return tickets

@router.get("/{ticket_id}", response_model=SDetailTicket)
async def get_detail_ticket(ticket_id: int):
    ticket = await TicketDAO.get_ticket_with_messages(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Тикет не найден")
    return ticket

"""@router.put("/{ticket_id}", response_model=SDetailTicket)
async def update_ticket(ticket_id: int, ticket_data: SDetailTicket):
    # Проверяем, существует ли тикет с указанным ID
    ticket = await TicketDAO.find_one_or_none(id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Тикет не найден")

    # Обновляем тикет в базе данных
    updated_ticket = await TicketDAO.update_ticket(ticket_id, ticket_data)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Тикет не обновлен")

    return updated_ticket"""

@router.post("/add_ticket", response_model=SCreateTicket)
async def create_ticket(ticket_data: SCreateTicket, attachments:UploadFile):
    # Создаем новый тикет в базе данных
    try:
        new_ticket = await TicketDAO.create_ticket(ticket_data, attachments)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not new_ticket:
        raise HTTPException(status_code=400, detail="Не удалось создать тикет")

    return new_ticket