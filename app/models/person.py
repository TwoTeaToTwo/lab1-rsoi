from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PersonModel(Base):
    __tablename__ = "persons"
    __table_args__ = (CheckConstraint("age >= 0", name="ck_persons_age_non_negative"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int | None] = mapped_column(nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    work: Mapped[str | None] = mapped_column(String(255), nullable=True)

