from datetime import datetime, timedelta 
from passlib.context import CryptContext
from jose import jwt

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITM)
    return encoded_jwt


async def authenticate_user(login: str, password: str):
    from app.users.dao import UserDAO
    user = await UserDAO.find_one_or_none(login=login)
    if user and verify_password(password, user.password):  # <-- или даже так
        return user