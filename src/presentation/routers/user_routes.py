from fastapi import HTTPException, Request

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.domain.models import UserModel, ResendVerificationRequest
from src.domain.repositories import UserRepository, get_async_db, CardRepository, CategoryRepository
from src.application.schemas import CreateUserSchema
from src.services.token_generator import generate_token
from src.services.email import EmailStr

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

@router.get("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_async_db)
):
    user = await UserRepository(db).read_by_verification_token(token)
    if not user:
        raise HTTPException(status_code=404, detail="Неверный токен")

    await UserRepository(db).update(user.id, {"is_verified": True})
    return {"message": "Email успешно подтвержден"}

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

@router.get("/{email}/categories")
async def get_categories_by_user(email: str, db: AsyncSession = Depends(get_async_db)):
    user = await UserRepository(db).read_by_email(email)
    print(user)
    if not user:
        return []
    return await CategoryRepository(db).read_by_user(user)

@router.post("/register")
async def register_user(
    user_data: CreateUserSchema,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    if await UserRepository(db).read_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    user = UserModel(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        is_verified=False,
        is_active=True,
        verification_token=generate_token()
    )
    created_user = await UserRepository(db).create(user)

    verification_link = f"http://localhost:8000/users/verify-email?token={user.verification_token}"
    await request.app.state.email_service.send_verification_email(
        user_data.email,
        verification_link
    )

    return created_user

@router.post("/resend-verification")
async def resend_verification(
    request_data: ResendVerificationRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    user = await UserRepository(db).read_by_email(request_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user.is_verified:
        return {"message": "Email уже подтвержден"}

    verification_link = f"http://localhost:8000/users/verify-email?token={user.verification_token}"
    await request.app.state.email_service.send_verification_email(request_data.email, verification_link)

    return {"message": "Письмо отправлено повторно"}