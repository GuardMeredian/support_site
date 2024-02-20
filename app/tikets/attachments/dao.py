from typing import TypeVar
from app.DAO.base import BaseDAO
from app.tikets.attachments.models import Attachments

T = TypeVar('T')

class AttachmentDAO(BaseDAO[Attachments]):
    model = Attachments

    