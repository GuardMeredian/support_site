from typing import TypeVar
from sqlalchemy import insert, select, update, delete
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User

T = TypeVar('T')

class UserDAO(BaseDAO[User]):
    model = User
        