from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from src.domain.models import Base

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///1.db"
DATABASE_URL = "sqlite:///1.db"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
engine = create_engine(DATABASE_URL)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)