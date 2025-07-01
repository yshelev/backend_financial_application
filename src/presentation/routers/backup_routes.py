from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.application.schemas import BackupSchema, GetBackupSchema
from src.domain.repositories import get_async_db, BackupRepository, UserRepository

router = APIRouter(prefix="/backup",
                   tags=["Backup"])


@router.put("/")
async def create_new_backup(backup_schema: BackupSchema, db: AsyncSession = Depends(get_async_db)):
	user = await UserRepository(db).read_by_email(backup_schema.user_email)
	await BackupRepository(db).upsert_backup(
		backup_data=backup_schema.data,
		user_id=user.id
	)

	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content={"status": "successfully created"}
	)


@router.get("/")
async def get_backup(schema: GetBackupSchema, db: AsyncSession = Depends(get_async_db)):
	user = await UserRepository(db).read_by_email(schema.email)
	return await BackupRepository(db).get_backup(user.id)
