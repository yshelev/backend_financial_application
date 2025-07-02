from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.domain.models import CardModel, CategoryModel
from src.domain.repositories import get_async_db, CardRepository, TransactionRepository, UserRepository
from src.application.schemas import CreateCardSchema, BalanceUpdateSchema, CreateCategorySchema

router = APIRouter(prefix="/categories",
                   tags=["Categories"])

router.get("/{category_id}")
async def get_category_by_id(transaction_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TransactionRepository(db).read_by_id(transaction_id)

@router.post("/")
async def create_category(category: CreateCategorySchema, db: AsyncSession = Depends(get_async_db)):
    cur_transaction = CategoryModel(**category.model_dump())
    return await TransactionRepository(db).create(cur_transaction)


@router.delete("/{category_id}")
async def delete_category(card_id: int, db: AsyncSession = Depends(get_async_db)):
    await TransactionRepository(db).delete(card_id)
