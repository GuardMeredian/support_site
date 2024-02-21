from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

eobd_engine = create_async_engine(settings.MS_SQL_CONNECTION_STRING)
eobd_async_session = sessionmaker(eobd_engine, expire_on_commit=False, class_=AsyncSession)



class Base(DeclarativeBase):
    pass

class EobdBase(DeclarativeBase):
    pass
    
    