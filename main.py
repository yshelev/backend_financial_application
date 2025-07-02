from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
import os

from src.domain.database import create_tables
from src.presentation.routers import cards_routes, transaction_routes, user_routes, categories_routes
from src.services.email import EmailService

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    pass

app = FastAPI(lifespan=lifespan)

email_service = EmailService(
    smtp_server="smtp.yandex.ru",
    port=465,
    username=os.getenv("EMAIL_ADDRESS"),
    password=os.getenv("EMAIL_PASSWORD")
)

app.state.email_service = email_service

app.include_router(cards_routes.router)
app.include_router(transaction_routes.router)
app.include_router(user_routes.router)
app.include_router(categories_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app")