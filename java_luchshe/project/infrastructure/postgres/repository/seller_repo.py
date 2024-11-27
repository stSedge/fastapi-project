from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.sellers import SellerCreateUpdateSchema, SellerSchema
from project.infrastructure.postgres.models import Seller

from project.core.config import settings
from project.core.exceptions import NotFound


class SellerRepository:
    _collection: Type[Seller] = Seller
    _type: str = "Seller"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_sellers(
        self,
        session: AsyncSession,
    ) -> list[SellerSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.sellers;"

        sellers = await session.execute(text(query))

        return [SellerSchema.model_validate(obj=seller) for seller in sellers.mappings().all()]

    async def get_seller_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> SellerSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        seller = await session.scalar(query)

        if not seller:
            raise NotFound(_object=f"{self._type}", _id=id)

        return SellerSchema.model_validate(obj=seller)

    async def create_seller(
            self,
            session: AsyncSession,
            seller1: SellerCreateUpdateSchema,
    ) -> SellerSchema:
        query = (
            insert(self._collection)
            .values(seller1.model_dump())
            .returning(self._collection)
        )
        created_seller = await session.scalar(query)
        await session.commit()

        return SellerSchema.model_validate(obj=created_seller)

    async def update_seller(
            self,
            session: AsyncSession,
            id: int,
            seller: SellerCreateUpdateSchema,
    ) -> SellerSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(seller.model_dump())
            .returning(self._collection)
        )

        updated_seller = await session.scalar(query)

        if not updated_seller:
            raise NotFound(_object=f"{self._type}", _id=id)

        return SellerSchema.model_validate(obj=updated_seller)

    async def delete_seller(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.sellers where id = {id};"

        seller = await session.execute(text(query))