from typing import List, Dict, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from app.EOBD.dao import EobddDAO
from app.users.dependescies import get_current_user
from app.exceptions import UserNotAuthException, UserIncorrectRoleException
from app.database import TEMP_async_session, TEST_async_session

router = APIRouter(
    prefix="/protocol",
    tags=["Протоколы"]
)

@router.get("/protocol39_amb/{chief}/{year}/{year_qr}", response_model=Dict[str, Any], name="Получить результат процедуры EOBD_PROTOCOL39_AMB", description="Вызвать хранимую процедуру EOBD_PROTOCOL39_AMB и получить результат")
async def get_protocol39_amb_result(
    chief: int,
    year: int,
    year_qr:int,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    if not current_user:
        raise UserNotAuthException
    user = current_user["User"]
    if user['role']['id'] == 2:
        raise UserIncorrectRoleException

    result = await EobddDAO.get_protocol(chief, year, year_qr)
    if not result:
        raise HTTPException(status_code=404, detail="Результат процедуры не найден")
    return result