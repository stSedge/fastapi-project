from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import date

from java_luchshe.project.infrastructure.postgres.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    total_sum: Mapped[int] = mapped_column(nullable=False)
    discount: Mapped[int] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)


class Seller(Base):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    data_start: Mapped[date] = mapped_column(nullable=False)
    data_end: Mapped[date] = mapped_column(nullable=True)


class TypeOfProduct(Base):
    __tablename__ = "type_of_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)


class AdditionalProduct(Base):
    __tablename__ = "additional_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    id_type: Mapped[int] = mapped_column(ForeignKey('type_of_product.id', ondelete='CASCADE'), nullable=False)


class Bouquet(Base):
    __tablename__ = "bouquets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    id_type: Mapped[int] = mapped_column(ForeignKey('type_of_product.id', ondelete='CASCADE'), nullable=False)
    size: Mapped[str] = mapped_column(nullable=True)


class Flower(Base):
    __tablename__ = "flowers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    id_type: Mapped[int] = mapped_column(ForeignKey('type_of_product.id', ondelete='CASCADE'), nullable=False)


class CompoundBouquet(Base):
    __tablename__ = "compound_bouquet"

    id_bouquet: Mapped[int] = mapped_column(ForeignKey('bouquets.id', ondelete='CASCADE'), primary_key=True)
    id_flower: Mapped[int] = mapped_column(ForeignKey('flowers.id', ondelete='CASCADE'), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)

class Supply(Base):
    __tablename__ = "supply"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_type: Mapped[int] = mapped_column(ForeignKey('type_of_product.id', ondelete='CASCADE'), nullable=False)
    id_product: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    id_seller: Mapped[int] = mapped_column(ForeignKey('sellers.id'), nullable=False)
    data: Mapped[date] = mapped_column(nullable=False)


class Selling(Base):
    __tablename__ = "selling"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_supply: Mapped[int] = mapped_column(ForeignKey('supply.id'), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    id_seller: Mapped[int] = mapped_column(ForeignKey('sellers.id'), nullable=False)
    discount: Mapped[int] = mapped_column(nullable=False)
    final_cost: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[date] = mapped_column(nullable=False)