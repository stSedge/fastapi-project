from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.type_of_products import TypeOfProductCreateUpdateSchema, TypeOfProductSchema
from project.infrastructure.postgres.models import TypeOfProduct

from project.core.config import settings
from project.core.exceptions import NotFound


class TypeOfProductRepository:
    _collection: Type[TypeOfProduct] = TypeOfProduct
    _type: str = "Type of product"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_type_of_products(
        self,
        session: AsyncSession,
    ) -> list[TypeOfProductSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.type_of_product;"

        type_of_products = await session.execute(text(query))

        return [TypeOfProductSchema.model_validate(obj=type_of_product) for type_of_product in type_of_products.mappings().all()]

    async def get_type_of_product_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> TypeOfProductSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        type_of_product = await session.scalar(query)

        if not type_of_product:
            raise NotFound(_object=f"{self._type}", _id=id)

        return TypeOfProductSchema.model_validate(obj=type_of_product)

    async def create_type_of_product(
            self,
            session: AsyncSession,
            type_of_product1: TypeOfProductCreateUpdateSchema,
    ) -> TypeOfProductSchema:
        query = (
            insert(self._collection)
            .values(type_of_product1.model_dump())
            .returning(self._collection)
        )
        created_type_of_product = await session.scalar(query)
        await session.commit()

        return TypeOfProductSchema.model_validate(obj=created_type_of_product)

    async def update_type_of_product(
            self,
            session: AsyncSession,
            id: int,
            type_of_product: TypeOfProductCreateUpdateSchema,
    ) -> TypeOfProductSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(type_of_product.model_dump())
            .returning(self._collection)
        )

        updated_type_of_product = await session.scalar(query)

        if not updated_type_of_product:
            raise NotFound(_object=f"{self._type}", _id=id)

        return TypeOfProductSchema.model_validate(obj=updated_type_of_product)

    async def delete_type_of_product(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.type_of_product where id = {id};"

        type_of_product = await session.execute(text(query))