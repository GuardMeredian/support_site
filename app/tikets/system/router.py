from typing import List
from fastapi import APIRouter, Depends
from app.exceptions import UserIncorrectRoleException, UserNotAuthException
from app.tikets.system.dao import SystemDAO
from app.tikets.system.models import System

from app.tikets.system.schemas import SSystem
from app.users.dependescies import get_current_user


router = APIRouter(
    prefix="/systems",
    tags=["Системы"])


@router.get("/", response_model=List[SSystem])
async def get_all_systems(current_user: dict = Depends(get_current_user)) -> List[SSystem]:
    if not current_user:
        raise UserNotAuthException
    
    systems = await SystemDAO.find_all()
    return systems
