from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	...

class UserModel(Base):
	__tablename__ = "users"
	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	username: Mapped[str] = mapped_column()
	password: Mapped[str] = mapped_column()