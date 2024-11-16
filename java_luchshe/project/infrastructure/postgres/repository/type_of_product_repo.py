from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.type_of_product import TypeOfProductSchema
from project.infrastructure.postgres.models import TypeOfProduct

from project.core.config import settings


class TypeOfProductRepository:
    _collection: Type[TypeOfProduct] = TypeOfProduct

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_types_of_products(
        self,
        session: AsyncSession,
    ) -> list[TypeOfProductSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.type_of_product;"

        typeOfProducts = await session.execute(text(query))

        return [TypeOfProductSchema.model_validate(obj=typeOfProduct) for typeOfProduct in typeOfProducts.mappings().all()]