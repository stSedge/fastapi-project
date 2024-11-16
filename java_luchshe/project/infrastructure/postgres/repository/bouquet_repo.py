from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.bouquets import BouquetSchema
from project.infrastructure.postgres.models import Bouquet

from project.core.config import settings


class BouquetRepository:
    _collection: Type[Bouquet] = Bouquet

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bouquets(
        self,
        session: AsyncSession,
    ) -> list[BouquetSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.bouquets;"

        bouquets = await session.execute(text(query))

        return [BouquetSchema.model_validate(obj=bouquet) for bouquet in bouquets.mappings().all()]