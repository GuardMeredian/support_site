from fastapi import APIRouter
from app.users.schemas import SUserRegister


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"]
)

router.post("/register")
async def register_user(user_data: SUserRegister):
    pass