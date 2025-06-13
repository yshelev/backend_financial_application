from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine
from src.models import Base, UserModel
from src.repositories import get_async_db, UserRepository
from src.schemas import UserSchema

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_all()

@app.post("/users")
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_async_db)):
    user_m = UserModel(**user.model_dump())
    return await UserRepository(db).create(user_m)

@app.get("/user/{username}")
async def get_user(username: str, db: AsyncSession = Depends(get_async_db)):
    return await UserRepository(db).read_by_username(username)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)