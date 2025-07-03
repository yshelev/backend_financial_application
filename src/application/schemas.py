import decimal
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, Field


class CreateUserSchema(BaseModel):
	username: str
	password: str
	email: EmailStr
	is_active: bool = True

class CreateTransactionSchema(BaseModel):
	is_income: bool
	amount: decimal.Decimal
	currency: str = "RUB"
	description: str = None
	card_id: int
	category_id: int
	date: int

class CreateCardSchema(BaseModel):
	masked_number: str
	name: str
	currency: str = "RUB"
	owner_id: int
	date: str
	balance: decimal.Decimal = decimal.Decimal("0")

class ExportTransactionDataSchema(BaseModel):
	...

class ExportCardDataSchema(BaseModel):
	name: str
	masked_number: str
	date: str
	currency: str
	balance: decimal.Decimal

class OutputTransactionSchema(BaseModel):
	is_income: bool
	amount: decimal.Decimal
	currency: str
	description: str = None
	category_id: int
	card_id: int
	date: int

	class Config:
		orm_mode = True

	@field_validator("date", mode="before")
	@classmethod
	def convert_date(cls, v):
		if isinstance(v, datetime):
			return int(v.timestamp() * 1000)
		return v

class OutputCardSchema(BaseModel):
	name: str
	masked_numer: str
	date: str
	currency: str
	balance: decimal.Decimal

class BackupDataSchema(BaseModel):
	transactions: list[OutputTransactionSchema]
	cards: list[OutputCardSchema]

class BackupSchema(BaseModel):
	user_email: EmailStr
	data: BackupDataSchema

class GetBackupSchema(BaseModel):
	email: str

class BalanceUpdateSchema(BaseModel):
	card_id: int
	new_balance: decimal.Decimal

class CreateCategorySchema(BaseModel):
	title: str
	icon_res_id: int
	user_id: int
	is_income: bool
	color: str