from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database import async_engine
from src.models import UserModel


async def get_async_db():
    async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def read_all(self):
        users = await self.session.execute(select(UserModel))
        return users.scalars().all()

    async def read_by_username(self, username: str):
        user = await self.session.execute(select(UserModel).where(UserModel.username == username))
        return user.scalar()

    async def create(self, user):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


