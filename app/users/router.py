from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from app.auth.auth import create_access_token
from app.users.schemas import SUserAuth
from app.auth.auth import authenticate_user


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"]
)

router.post("/login")
async def login_user(response: Response, user_data:Annotated[SUserAuth, Depends()]):
    user = await authenticate_user(user_data.login, user_data.password)
    if not user:
        raise HTTPException(401)
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("user_access", access_token, httponly=True)
    return{"token":access_token}