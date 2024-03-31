from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./img_api.db"

engine = create_async_engine(
    SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

Base = declarative_base()


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
