from pydantic import BaseModel, EmailStr, field_validator

from src.models import UserModel


class CreateUserSchema(BaseModel):
	username: str
	password: str
	email: EmailStr
	is_active: bool = False

class CreateTransactionSchema(BaseModel):
	...

class CreateCardSchema(BaseModel):
	masked_number: str
	name: str
	currency: str = "RUB"
	user: UserModel

	@field_validator('masked_number')
	def validate_card_number_format(self, v: str) -> str:
		if not v.isdigit():
			raise ValueError('Номер карты должен состоять только из цифр.')

		if len(v) != 4:
			raise ValueError('Номер карты должен состоять ровно из 4 цифр.')

		return v
