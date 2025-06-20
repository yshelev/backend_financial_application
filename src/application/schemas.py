import decimal
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, field_validator

class CreateUserSchema(BaseModel):
	username: str
	password: str
	email: EmailStr
	is_active: bool = True

class CreateTransactionSchema(BaseModel):
	is_income: bool
	amount: decimal.Decimal
	currency: str = "RUB"
	icon_res_id: int
	description: str = None
	card_id: int

class CreateCardSchema(BaseModel):
	masked_number: str
	name: str
	currency: str = "RUB"
	owner_id: int
	date: date

	@field_validator('masked_number')
	@staticmethod
	def validate_card_number_format(v: str) -> str:
		if not v.isdigit():
			raise ValueError('Номер карты должен состоять только из цифр.')

		if len(v) != 4:
			raise ValueError('Номер карты должен состоять ровно из 4 цифр.')

		return v

	@field_validator('date')
	@staticmethod
	def validate_date_format(v):
		try:
			datetime.strptime(f"2000-{v}", "%Y-%m-%d")
			return v
		except ValueError:
			raise ValueError("Дата должна быть в формате MM-DD")
