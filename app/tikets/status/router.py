from typing import List
from fastapi import APIRouter, Depends
from app.exceptions import UserIncorrectRoleException, UserNotAuthException
from app.tikets.status.dao import StatusDAO
from app.tikets.status.models import Status

from app.tikets.status.schemas import SStatus
from app.users.dependescies import get_current_user


router = APIRouter(
    prefix="/statuses",
    tags=["Статусы"])


@router.get("/", response_model=List[SStatus], name="Получить список статусов", description="Получить список возможных статусов для заявок")
async def get_all_status(current_user: dict = Depends(get_current_user)) -> List[Status]:
    if not current_user:
        raise UserNotAuthException
    
    user = current_user["User"]
    if user['role']['id'] == 2:
        raise UserIncorrectRoleException
    statuses = await StatusDAO.find_all()
    return statuses
