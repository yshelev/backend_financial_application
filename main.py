from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine
from src.models import *
from src.repositories import get_async_db, UserRepository, TransactionRepository, CardRepository
from src.schemas import CreateUserSchema, CreateTransactionSchema, CreateCardSchema

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/transactions/{transaction_id}")
async def get_transaction_by_id(transaction_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TransactionRepository(db).read_by_id(transaction_id)

@app.post("/transactions")
async def create_transaction(transaction: CreateTransactionSchema, db: AsyncSession = Depends(get_async_db)):
    return await TransactionRepository(db).create(**transaction.model_dump())

@app.get("cards/{card_id}/transactions")
async def get_transactions_by_card(card_id: int, db: AsyncSession = Depends(get_async_db)):
    card = await CardRepository(db).read_by_id(card_id)
    return await TransactionRepository(db).read_by_card(card)

@app.get("/cards/{card_id}")
async def get_card_by_id(card_id: int, db: AsyncSession = Depends(get_async_db)):
    return await CardRepository(db).read_by_id(card_id)

@app.post("/cards")
async def create_transaction(card: CreateCardSchema, db: AsyncSession = Depends(get_async_db)):
    return await CardRepository(db).create(**card.model_dump())

@app.get("/user/{username}/cards")
async def get_cards_by_user(username: str, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_username(username)
    return await CardRepository(db).read_by_user(user)


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_all()

@app.post("/users")
async def create_user(user: CreateUserSchema, db: AsyncSession = Depends(get_async_db)):
    user_m = UserModel(**user.model_dump())
    return await UserRepository(db).create(user_m)

@app.get("/user/{username}")
async def get_user(username: str, db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_by_username(username)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app)