from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.domain.models import UserModel
from src.domain.repositories import UserRepository, get_async_db, CardRepository
from src.application.schemas import CreateUserSchema

router = APIRouter(prefix="/users",
                   tags=["Users"])

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_all()

@router.get("/{email}/transactions")
async def get_transactions_by_user(email: str, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_email_with_cards_and_transactions(email)
    if not user:
        return []
    cards = user.cards
    output = []

    for card in cards:
        output.extend(card.transactions)

    return output

@router.post("/")
async def create_user(user: CreateUserSchema, db: AsyncSession = Depends(get_async_db)):
    user_m = UserModel(**user.model_dump())
    return await UserRepository(db).create(user_m)

@router.get("/{email}")
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_email(email)
    return user

@router.get("/{id}")
async def get_user_by_id(id_: int, db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_by_id(id_)

@router.get("/{email}/cards")
async def get_cards_by_user(email: str, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_email(email)
    if not user:
        return []
    return await CardRepository(db).read_by_user(user)