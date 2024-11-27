from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.compound_bouquet import CompoundBouquetSchema
from project.infrastructure.postgres.models import CompoundBouquet

from project.core.config import settings
from project.core.exceptions import NotFound


class CompoundBouquetRepository:
    _collection: Type[CompoundBouquet] = CompoundBouquet
    _type : str = "Compound Bouquet"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_compound_bouquets(
        self,
        session: AsyncSession,
    ) -> list[CompoundBouquetSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.compound_bouquet;"

        compound_bouquets = await session.execute(text(query))

        return [CompoundBouquetSchema.model_validate(obj=compound_bouquet) for compound_bouquet in compound_bouquets.mappings().all()]

    async def get_compound_bouquet_by_id(
        self,
        session: AsyncSession,
        id_bouquet: int,
        id_flower: int,
    ) -> CompoundBouquetSchema:
        query = (
            select(self._collection)
            .where(self._collection.id_bouquet == id_bouquet and self._collection.id_flower == id_flower)
        )

        compound_bouquet = await session.scalar(query)

        if not compound_bouquet:
            raise NotFound(_object=f"{self._type} {id_bouquet}", _id=id_flower)

        return CompoundBouquetSchema.model_validate(obj=compound_bouquet)

    async def create_compound_bouquet(
            self,
            session: AsyncSession,
            compound_bouquet1: CompoundBouquetSchema,
    ) -> CompoundBouquetSchema:
        query = (
            insert(self._collection)
            .values(compound_bouquet1.model_dump())
            .returning(self._collection)
        )
        created_compound_bouquet = await session.scalar(query)
        await session.commit()

        return CompoundBouquetSchema.model_validate(obj=created_compound_bouquet)

    async def update_compound_bouquet(
            self,
            session: AsyncSession,
            id_bouquet: int,
            id_flower: int,
            count: int
    ) -> CompoundBouquetSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_bouquet == id_bouquet and self._collection.id_flower == id_flower)
            .values(count=count)
            .returning(self._collection)
        )

        updated_compound_bouquet = await session.scalar(query)

        if not updated_compound_bouquet:
            raise NotFound(_object=f"{self._type} {id_bouquet}", _id=id_flower)

        return CompoundBouquetSchema.model_validate(obj=updated_compound_bouquet)

    async def delete_compound_bouquet(
        self,
        session: AsyncSession,
        id_bouquet: int,
        id_flower: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.compound_bouquet where id_flower = {id_flower} and id_bouquet = {id_bouquet};"

        compound_bouquet = await session.execute(text(query))

