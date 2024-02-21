from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class SNews(BaseModel):
    title: str
    content: str
    created_at: Optional[datetime] = None
    

    class Config:
        from_attributes = True