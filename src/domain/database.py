from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///../test.db"
DATABASE_URL = "sqlite:///../test.db"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
engine = create_engine(DATABASE_URL)