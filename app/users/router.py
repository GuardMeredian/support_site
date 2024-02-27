from typing import List
from fastapi import APIRouter, Depends, Response
from app.users.auth import create_access_token
from app.exceptions import UserIncorrectRoleException, UserIsNotPresentException, UserNotAuthException
from app.users.dao import UserDAO
from app.users.dependescies import get_current_user
from app.users.models import User
from app.users.schemas import SUserAuth, SUserForMsg
from app.users.auth import authenticate_user
from app.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)

@router.post("/login")
async def login_user(response: Response, user_data:SUserAuth):
    user = await authenticate_user(user_data.login, user_data.password)
    if not user:
        raise UserIsNotPresentException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(settings.COOCKIES_NAME_TOKEN, access_token)
    return{"token":access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(settings.COOCKIES_NAME_TOKEN)
    return {"msg":"Вы покинули сервис"}

@router.get("/user")
async def get_user(user: User = Depends(get_current_user)):
    return user

@router.get("/users", response_model=List[SUserForMsg])
async def get_all_status(current_user: dict = Depends(get_current_user)) -> List[User]:
    if not current_user:
        raise UserNotAuthException
    
    user = current_user["User"]
    if user['role']['id'] == 2:
        raise UserIncorrectRoleException
    users = await UserDAO.find_all(role_id=3)
    return users
