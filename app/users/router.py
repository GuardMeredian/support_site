from fastapi import APIRouter, Depends, Response
from app.users.auth import create_access_token
from app.exceptions import UserIsNotPresentException
from app.users.schemas import SUserAuth
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