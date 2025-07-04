from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.domain.models import CardModel
from src.domain.repositories import get_async_db, CardRepository, TransactionRepository, UserRepository
from src.application.schemas import CreateCardSchema, BalanceUpdateSchema

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
    card_m = CardModel(**card.model_dump())
    return await CardRepository(db).create(card_m)

@router.delete("/{card_id}")
async def delete_card(card_id: int, db: AsyncSession = Depends(get_async_db)):
    await CardRepository(db).delete(card_id)
    return HTTP_200_OK

@router.patch("/")
async def patch_card(update_schema: BalanceUpdateSchema, db: AsyncSession = Depends(get_async_db)):
    return await CardRepository(db).patch_card(update_schema.card_id,
                                        update_schema.new_balance)
