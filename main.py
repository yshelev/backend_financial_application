from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.domain.database import engine, create_tables
from src.presentation.routers import cards_routes, transaction_routes, user_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(cards_routes.router)
app.include_router(transaction_routes.router)
app.include_router(user_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="0.0.0.0")