from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.bouquets import BouquetCreateUpdateSchema, BouquetSchema
from project.infrastructure.postgres.models import Bouquet

from project.core.config import settings
from project.core.exceptions import NotFound


class BouquetRepository:
    _collection: Type[Bouquet] = Bouquet
    _type: str = "Bouquet"

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

    async def get_bouquet_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> BouquetSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        bouquet = await session.scalar(query)

        if not bouquet:
            raise NotFound(_object=f"{_type}", _id=id)

        return BouquetSchema.model_validate(obj=bouquet)

    async def create_bouquet(
            self,
            session: AsyncSession,
            bouquet1: BouquetCreateUpdateSchema,
    ) -> BouquetSchema:
        query = (
            insert(self._collection)
            .values(**bouquet1.model_dump(), id_type=2)
            .returning(self._collection)
        )
        created_bouquet = await session.scalar(query)
        await session.commit()

        return BouquetSchema.model_validate(obj=created_bouquet)

    async def update_bouquet(
            self,
            session: AsyncSession,
            id: int,
            bouquet: BouquetCreateUpdateSchema,
    ) -> BouquetSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(bouquet.model_dump())
            .returning(self._collection)
        )

        updated_bouquet = await session.scalar(query)

        if not updated_bouquet:
            raise NotFound(_object=f"{self._type}", _id=id)

        return BouquetSchema.model_validate(obj=updated_bouquet)

    async def delete_bouquet(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.bouquets where id = {id};"

        bouquet = await session.execute(text(query))