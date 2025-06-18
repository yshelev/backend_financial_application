from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import UserModel
from src.domain.repositories import UserRepository, get_async_db, CardRepository
from src.application.schemas import CreateUserSchema

router = APIRouter(prefix="/users",
                   tags=["Users"])

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_all()

@router.post("/")
async def create_user(user: CreateUserSchema, db: AsyncSession = Depends(get_async_db)):
    user_m = UserModel(**user.model_dump())
    return await UserRepository(db).create(user_m)

@router.get("/{username}")
async def get_user(username: str, db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_by_username(username)

@router.get("/{username}/cards")
async def get_cards_by_user(username: str, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_username(username)
    return await CardRepository(db).read_by_user(user)