from sqlalchemy.orm import Mapped, mapped_column

from java_luchshe.project.infrastructure.postgres.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    total_sum: Mapped[str] = mapped_column(nullable=False)
    discount: Mapped[str] = mapped_column(nullable=True)