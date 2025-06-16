from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database import async_engine
from src.models import UserModel, TransactionModel, CardModel
from src.schemas import CreateTransactionSchema


async def get_async_db():
    async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

class AsyncRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

class UserRepository(AsyncRepository):
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


class TransactionRepository(AsyncRepository):
    async def read_by_id(self, transaction_id: int):
        transaction = await self.session.execute(select(TransactionModel).where(TransactionModel.id == transaction_id))
        return transaction.scalar()

    async def read_by_card(self, card: CardModel):
        transactions = await self.session.execute(select(TransactionModel).where(TransactionModel.card == card))
        return transactions.scalars().all()

    async def create(self, transaction):
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

class CardRepository(AsyncRepository):
    async def read_by_id(self, card_id: int):
        card = await self.session.execute(select(CardModel).where(CardModel.id == card_id))
        return card.scalar()

    async def read_by_user(self, user: UserModel):
        cards = await self.session.execute(select(CardModel).where(CardModel.user == user))
        return cards.scalars().all()

    async def create(self, card):
        self.session.add(card)
        await self.session.commit()
        await self.session.refresh(card)
        return card
