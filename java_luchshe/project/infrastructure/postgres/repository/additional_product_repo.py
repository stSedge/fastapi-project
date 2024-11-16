from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.additional_products import AddProductSchema
from project.infrastructure.postgres.models import AdditionalProduct

from project.core.config import settings


class AdditionalProductRepository:
    _collection: Type[AdditionalProduct] = AdditionalProduct

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
    ) -> list[AddProductSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.additional_products;"

        additional_products = await session.execute(text(query))

        return [AddProductSchema.model_validate(obj=additional_product) for additional_product in additional_products.mappings().all()]