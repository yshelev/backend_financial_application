import decimal

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
	icon_res_id: int
	description: str = None
	card_id: int

class CreateCardSchema(BaseModel):
	masked_number: str
	name: str
	currency: str = "RUB"
	owner_email: EmailStr = Field(..., exclude=True)
	date: str
	balance: float = 0

	# @field_validator('masked_number')
	# def validate_card_number_format(self, v: str) -> str:
	# 	if not v.isdigit():
	# 		raise ValueError('Номер карты должен состоять только из цифр.')
	#
	# 	if len(v) != 4:
	# 		raise ValueError('Номер карты должен состоять ровно из 4 цифр.')
	#
	# 	return v