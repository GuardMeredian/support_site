from pydantic import BaseModel
from typing import Optional
from datetime import date



class SPeriod(BaseModel):
    LPUCODE: Optional[int]
    DATE_BEG: Optional[date]
    DATE_END: Optional[date]
    STATUS: Optional[int]
    NAME: Optional[str]
    YEAR: Optional[int]
    MODE: Optional[int]
    NUMBER_PER: Optional[int]
    TYPE_LPU: Optional[int]
    VDATE1: Optional[date]
    VDATE2: Optional[date]

    class Config:
        from_attributes = True


