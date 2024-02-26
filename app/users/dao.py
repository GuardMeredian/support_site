from typing import TypeVar
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User

T = TypeVar('T')

class UserDAO(BaseDAO[User]):
    model = User
        

    @classmethod
    async def find_by_id_user(cls, model_id: int):
        async with async_session_maker() as session:
            # Запрос для получения пользователя с определенными полями и связанной ролью
            user_query = select(cls.model).options(joinedload(cls.model.role)).filter_by(id=model_id)
            user_result = await session.execute(user_query)
            user = user_result.scalars().first()


            # Получаем роль пользователя
            role = user.role

        # Создаем новый словарь с полями пользователя и ролью
        user_with_role = {
            'id': user.id,
            'surname': user.surname,
            'name': user.name,
            'secname': user.secname,
            'role':{
                'id': role.id,
                'description':role.description
            }  
        }
        return user_with_role