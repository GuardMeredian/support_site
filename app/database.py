from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

eobd_engine = create_async_engine(settings.MS_SQL_CONNECTION_STRING)
eobd_async_session = sessionmaker(eobd_engine, expire_on_commit=False, class_=AsyncSession)

AKTPAK_engine = create_async_engine(settings.AKTPAK_MS_SQL_CONNECTION_STRING)
AKTPAK_async_session = sessionmaker(AKTPAK_engine, expire_on_commit=False, class_=AsyncSession)

TEMP_engine = create_async_engine(settings.TEMP_MS_SQL_CONNECTION_STRING)
TEMP_async_session = sessionmaker(TEMP_engine, expire_on_commit=False, class_=AsyncSession)

TEST_engine = create_async_engine(settings.TEST_MS_SQL_CONNECTION_STRING)
TEST_async_session = sessionmaker(TEST_engine, expire_on_commit=False, class_=AsyncSession)



Base = declarative_base()
EobdBase = declarative_base()
AKTPAKBase = declarative_base()

#class Base(DeclarativeBase):
    #pass

#class EobdBase(DeclarativeBase):
    #pass
    
    