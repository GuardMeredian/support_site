from pydantic import BaseModel
from typing import Optional
from datetime import date



class SPeriod(BaseModel):
    LPUCODE: str
    DATE_BEG: date
    DATE_END: date
    STATUS: str
    NAME: str
    YEAR: int
    MODE: str
    NUMBER_PER: int
    TYPE_LPU: str
    VDATE1: date
    VDATE2: date

    class Config:
        from_attributes = True


