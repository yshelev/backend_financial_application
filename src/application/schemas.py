import decimal
from pydantic import BaseModel, EmailStr, field_validator

class CreateUserSchema(BaseModel):
	username: str
	password: str
	email: EmailStr
	is_active: bool = False

class CreateTransactionSchema(BaseModel):
	is_income: bool
	amount: decimal.Decimal
	currency: str = "RUB"

	card_id: int

class CreateCardSchema(BaseModel):
	masked_number: str
	name: str
	currency: str = "RUB"
	owner_id: int

	@field_validator('masked_number')
	@staticmethod
	def validate_card_number_format(v: str) -> str:
		if not v.isdigit():
			raise ValueError('Номер карты должен состоять только из цифр.')

		if len(v) != 4:
			raise ValueError('Номер карты должен состоять ровно из 4 цифр.')

		return v
