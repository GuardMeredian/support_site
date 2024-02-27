from typing import List, TypeVar
from app.tikets.system.models import System
from app.database import async_session_maker
from app.DAO.base import BaseDAO

T = TypeVar('T')

class SystemDAO(BaseDAO[System]):
    model = System