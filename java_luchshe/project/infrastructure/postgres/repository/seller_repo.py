from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.sellers import SellerSchema
from project.infrastructure.postgres.models import Seller

from project.core.config import settings


class SellerRepository:
    _collection: Type[Seller] = Seller

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