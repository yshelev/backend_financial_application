from fastapi import FastAPI

from src.domain.database import engine
from src.domain.models import *
from src.presentation.routers import cards_routes, transaction_routes, user_routes

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(cards_routes.router)
app.include_router(transaction_routes.router)
app.include_router(user_routes.router)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")