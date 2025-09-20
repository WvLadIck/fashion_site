from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

class BaseModel(DeclarativeBase):
    pass

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DEBUG,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

from app.models import *