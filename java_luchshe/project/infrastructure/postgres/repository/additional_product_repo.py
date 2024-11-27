from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.additional_products import AdditionalProductCreateUpdateSchema, AdditionalProductSchema
from project.infrastructure.postgres.models import AdditionalProduct

from project.core.config import settings
from project.core.exceptions import NotFound


class AdditionalProductRepository:
    _collection: Type[AdditionalProduct] = AdditionalProduct
    _type: str = "Additional product"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_additional_products(
        self,
        session: AsyncSession,
    ) -> list[AdditionalProductSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.additional_products;"

        additional_products = await session.execute(text(query))

        return [AdditionalProductSchema.model_validate(obj=additional_product) for additional_product in additional_products.mappings().all()]

    async def get_additional_product_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> AdditionalProductSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        additional_product = await session.scalar(query)

        if not additional_product:
            raise NotFound(_object=f"{self._type}", _id=id)

        return AdditionalProductSchema.model_validate(obj=additional_product)

    async def create_additional_product(
            self,
            session: AsyncSession,
            additional_product1: AdditionalProductCreateUpdateSchema,
    ) -> AdditionalProductSchema:
        query = (
            insert(self._collection)
            .values(**additional_product1.model_dump(), id_type=3)
            .returning(self._collection)
        )
        created_additional_product = await session.scalar(query)
        await session.commit()

        return AdditionalProductSchema.model_validate(obj=created_additional_product)

    async def update_additional_product(
            self,
            session: AsyncSession,
            id: int,
            additional_product: AdditionalProductCreateUpdateSchema,
    ) -> AdditionalProductSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(additional_product.model_dump())
            .returning(self._collection)
        )

        updated_additional_product = await session.scalar(query)

        if not updated_additional_product:
            raise NotFound(_object=f"{self._type}", _id=id)

        return AdditionalProductSchema.model_validate(obj=updated_additional_product)

    async def delete_additional_product(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.additional_products where id = {id};"

        additional_product = await session.execute(text(query))