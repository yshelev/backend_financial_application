from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload

from src.application.schemas import BackupSchema, BackupDataSchema
from src.domain.database import async_engine
from src.domain.models import UserModel, TransactionModel, CardModel, BackupModel, CategoryModel


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

    async def read_by_id(self, id_: int) -> UserModel:
        user = await self.session.execute(select(UserModel).where(UserModel.id == id_))
        return user.scalar()

    async def read_by_email_with_cards_and_transactions(self, email: str):
        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.cards)
                .selectinload(CardModel.transactions)
            )
            .where(UserModel.email == email)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def read_by_email(self, email: str):
        user = await self.session.execute(select(UserModel).where(UserModel.email == email))
        return user.scalar()
    
    async def read_by_verification_token(self, token: str) -> UserModel | None:
        print(f"TOKEN {token}")
        result = await self.session.execute(
            select(UserModel).where(UserModel.verification_token == token)
        )
        return result.scalars().first()

    async def create(self, user):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(self, user_id: int, update_data: dict) -> UserModel:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id))
        user = result.scalars().first()
        
        if not user:
            raise ValueError("User not found")
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
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

    async def delete(self, transaction_id):
        trns = await self.session.execute(delete(TransactionModel).where(TransactionModel.id == transaction_id))
        await self.session.commit()

class CardRepository(AsyncRepository):
    async def read_by_id(self, card_id: int):
        card = await self.session.execute(select(CardModel).where(CardModel.id == card_id))
        return card.scalar()

    async def read_by_user(self, user: UserModel):
        cards = await self.session.execute(select(CardModel).where(CardModel.owner_id == user.id))
        return cards.scalars().all()

    async def create(self, card):
        self.session.add(card)
        await self.session.commit()
        await self.session.refresh(card)
        return card

    async def delete(self, card_id):
        await self.session.execute(delete(CardModel).where(CardModel.id == card_id))
        await self.session.commit()

    async def patch_card(self, card_id, new_balance):
        card = (await self.session.execute(select(CardModel).where(CardModel.id == card_id))).scalar()
        card.balance = new_balance
        await self.session.commit()
        await self.session.refresh(card)
        return card

class BackupRepository(AsyncRepository):
    async def upsert_backup(self, backup_data: BackupDataSchema, user_id: int):
        query = (select(BackupModel)
                 .where(BackupModel.user_id == user_id)
                 .order_by(BackupModel.date))
        backup = (await self.session.execute(query)).scalar_one_or_none()

        if backup:
            query = (update(BackupModel)
                    .where(BackupModel.user_id == user_id)
                    .values(**{"data": backup_data.model_dump()}))
        else:
            query = (insert(BackupModel)
                     .values(**{
                            "user_id": user_id,
                            "data": backup_data.model_dump()
                    }))

        await self.session.execute(query)
        await self.session.commit()
        return

    async def get_backup(self, user_id: int):
        query = (select(BackupModel)
                 .where(BackupModel.user_id == user_id)
                 .order_by(BackupModel.date))
        return (await self.session.execute(query)).scalar_one_or_none()

class CategoryRepository(AsyncRepository):
    async def read_by_id(self, card_id: int):
        category = await self.session.execute(select(CategoryModel).where(CategoryModel.id == card_id))
        return category.scalar()

    async def read_by_user(self, user: UserModel):
        categories = await self.session.execute(select(CategoryModel).where(CategoryModel.user_id == user.id))
        return categories.scalars().all()

    async def create(self, category):
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category_id):
        await self.session.execute(delete(CategoryModel).where(CategoryModel.id == category_id))
        await self.session.commit()