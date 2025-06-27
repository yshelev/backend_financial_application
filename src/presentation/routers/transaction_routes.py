from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import TransactionModel
from src.domain.repositories import TransactionRepository, get_async_db
from src.application.schemas import CreateTransactionSchema

router = APIRouter(prefix="/transactions",
                   tags=["Transactions"])


@router.get("/{transaction_id}")
async def get_transaction_by_id(transaction_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TransactionRepository(db).read_by_id(transaction_id)

@router.post("/")
async def create_transaction(transaction: CreateTransactionSchema, db: AsyncSession = Depends(get_async_db)):
    cur_transaction = TransactionModel(**transaction.model_dump())
    return await TransactionRepository(db).create(cur_transaction)


@router.delete("/{card_id}")
async def delete_card(card_id: int, db: AsyncSession = Depends(get_async_db)):
    await TransactionRepository(db).delete(card_id)
