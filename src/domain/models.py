import decimal
from datetime import datetime, date

from sqlalchemy import String, DateTime, func, Numeric, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

currencies = ["RUB", "USD", "EUR"]

class Base(DeclarativeBase):
	...

class UserModel(Base):
	__tablename__ = "users"
	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str] = mapped_column(String(50))
	password: Mapped[str] = mapped_column()
	email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	registration_data: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=func.now()
	)
	is_active: Mapped[bool] = mapped_column()

	cards: Mapped[list["CardModel"]] = relationship(
		back_populates="owner",
		cascade="all, delete-orphan"
	)

	categories: Mapped[list["CategoryModel"]] = relationship(
		back_populates="user",
		cascade="all, delete-orphan"
	)


class TransactionModel(Base):
	__tablename__ = "transactions"
	id: Mapped[int] = mapped_column(primary_key=True)
	is_income: Mapped[bool] = mapped_column()
	amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3))
	currency: Mapped[str] = mapped_column()

	description: Mapped[str] = mapped_column(None)
	icon_res_id: Mapped[int] = mapped_column(None)

	card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
	card: Mapped["CardModel"] = relationship(back_populates="transactions")


class CardModel(Base):
	__tablename__ = "cards"
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column()
	masked_number: Mapped[str] = mapped_column(String(4))
	date: Mapped[str] = mapped_column(String(5))
	currency: Mapped[str] = mapped_column()
	balance: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), default=decimal.Decimal("0"))

	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

	owner: Mapped["UserModel"] = relationship(back_populates="cards")
	transactions: Mapped[list["TransactionModel"]] = relationship(
		back_populates="card",
		cascade="all, delete-orphan"
	)

class CategoryModel(Base):
	__tablename__ = "categories"
	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str] = mapped_column()
	icon_url: Mapped[str] = mapped_column()
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	user: Mapped["UserModel"] = relationship(back_populates="categories")