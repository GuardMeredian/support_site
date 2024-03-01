from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.news.models import News
from app.news.schemas import SNews
from app.news.dao import NewsDAO
from app.users.dependescies import get_current_user
from app.exceptions import UserIncorrectRoleException, UserNotAuthException, NewsIsNotAddException

router = APIRouter(
    prefix="/news",
    tags=["Новости"]
)

@router.get("/news", response_model=List[SNews], name="Получить все новости", description="Получить список всех новостей")
async def get_all_news(current_user: dict = Depends(get_current_user)) -> List[News]:
    if not current_user:
        raise UserNotAuthException
    
    news = await NewsDAO.get_news_list()
    return news

@router.post("/add_news", response_model=SNews, name="Добавить новость", description="Добавить новую новость в систему")
async def create_news(news_data: Annotated[SNews, Depends()], current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise UserNotAuthException
    
    user = current_user["User"]

    if user.role_id == 2 or user.role_id == 1:
        try:
            new_news = await NewsDAO.create_news(news_data)
        except:
            raise NewsIsNotAddException

        if not new_news:
            raise NewsIsNotAddException
        
        return new_news
    else:
        raise UserIncorrectRoleException