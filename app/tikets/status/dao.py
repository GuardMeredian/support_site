from typing import List, TypeVar
from app.tikets.status.models import Status
from app.database import async_session_maker
from app.DAO.base import BaseDAO

T = TypeVar('T')

class StatusDAO(BaseDAO[Status]):
    model = Status