from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
	username: str
	password: str
	email: EmailStr
	is_active: bool = False

class CreateTransactionSchema(BaseModel):
	...

class CreateCardSchema(BaseModel):
	...
