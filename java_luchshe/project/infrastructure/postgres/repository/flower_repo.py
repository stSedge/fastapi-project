from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.flowers import FlowerSchema
from project.infrastructure.postgres.models import Flower

from project.core.config import settings


class FlowerRepository:
    _collection: Type[Flower] = Flower

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_flowers(
        self,
        session: AsyncSession,
    ) -> list[FlowerSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.flowers;"

        flowers = await session.execute(text(query))

        return [FlowerSchema.model_validate(obj=flower) for flower in flowers.mappings().all()]