from fastapi import HTTPException, status


class SupportException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
    

class UserNotAuthException(SupportException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Пользователь не авторизован"


class UserIncorrectRoleException(SupportException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Пользователь не имеет прав доступа"

class TokenExpiredException(SupportException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истёк"

class TokenAbsentException(SupportException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class IncorrectTokenFormatException(SupportException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Некорректный формат токена"

class UserIsNotPresentException(SupportException):
    status_code=status.HTTP_401_UNAUTHORIZED

class OrgIsNotFoundException(SupportException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Организация не найдена"

class TicketIsNotFoundException(SupportException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Заявка не найдена"

class TicketIsNotAddException(SupportException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Не удалось создать заявку"

class TicketIsNotUpdateException(SupportException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Не удалось обновить заявку"

class MessageIsNotAddException(SupportException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Не удалось оставить сообщение"