from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import EobdBase

class Period(EobdBase):
    __tablename__ = 'RPERIOD'
    #__table_args__ = {'bind': eobd_engine}

    COUNTER: Mapped[int] = mapped_column(primary_key=True)
    LPUCODE: Mapped[int]
    DATE_BEG: Mapped[date]
    DATE_END: Mapped[date]
    D_START: Mapped[datetime]
    D_FIN: Mapped[datetime]
    D_MODIF: Mapped[datetime]
    STATUS: Mapped[str]
    NAME: Mapped[str]
    YEAR: Mapped[int]
    MODE: Mapped[str]
    NUMBER_PER: Mapped[int]
    TYPE_LPU: Mapped[str]
    COUNTER_AP: Mapped[int]
    DATE_APR: Mapped[datetime]
    VDATE1: Mapped[date]
    VDATE2: Mapped[date]
    COUNTER_A2: Mapped[int]
    DATE_APR_M: Mapped[datetime]
    COMMENTS: Mapped[str]
    IS_KMIS: Mapped[bool]

    # Отношения с другими моделями, если они есть
    # tickets = relationship("Ticket", back_populates="period")
    # users = relationship("User", back_populates="period")

    def __str__(self):
        return f"{self.NAME} ({self.COUNTER})"