from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.EOBD.Period.models import Period
from app.EOBD.Period.schemas import SPeriod
from app.EOBD.Period.dao import PeriodDAO
from app.users.dependescies import get_current_user
from app.exceptions import UserIncorrectRoleException, UserNotAuthException, NewsIsNotAddException

router = APIRouter(
    prefix="/periods",
    tags=["Периоды"]
)

@router.get("/", response_model=List[SPeriod], name="Получить все периоды", description="Получить список всех периодов")
async def get_all_periods(current_user: dict = Depends(get_current_user)) -> List[Period]:
    if not current_user:
        raise UserNotAuthException
    
    periods = await PeriodDAO.get_period_list()
    return periods