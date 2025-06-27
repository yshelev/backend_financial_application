from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import CardModel
from src.domain.repositories import get_async_db, CardRepository, TransactionRepository, UserRepository
from src.application.schemas import CreateCardSchema

router = APIRouter(prefix="/cards",
                   tags=["Cards"])

@router.get("/{card_id}/transactions")
async def get_transactions_by_card(card_id: int, db: AsyncSession = Depends(get_async_db)):
    card = await CardRepository(db).read_by_id(card_id)
    return await TransactionRepository(db).read_by_card(card)

@router.get("/{card_id}")
async def get_card_by_id(card_id: int, db: AsyncSession = Depends(get_async_db)):
    return await CardRepository(db).read_by_id(card_id)

@router.post("/")
async def create_transaction(card: CreateCardSchema, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_email(card.owner_email)
    card_m = CardModel(**card.model_dump(), owner_id=user.id)
    return await CardRepository(db).create(card_m)