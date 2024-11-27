from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.supply import SupplyCreateUpdateSchema, SupplySchema
from project.infrastructure.postgres.models import Supply

from project.core.config import settings
from project.core.exceptions import NotFound


class SupplyRepository:
    _collection: Type[Supply] = Supply
    _type: str = "Supply"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_supply(
        self,
        session: AsyncSession,
    ) -> list[SupplySchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.supply;"

        supplys = await session.execute(text(query))

        return [SupplySchema.model_validate(obj=supply) for supply in supplys.mappings().all()]

    async def get_supply_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> SupplySchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        supply = await session.scalar(query)

        if not supply:
            raise NotFound(_object=f"{self._type}", _id=id)

        return SupplySchema.model_validate(obj=supply)

    async def create_supply(
            self,
            session: AsyncSession,
            supply1: SupplyCreateUpdateSchema,
    ) -> SupplySchema:
        query = (
            insert(self._collection)
            .values(supply1.model_dump())
            .returning(self._collection)
        )
        created_supply = await session.scalar(query)
        await session.commit()

        return SupplySchema.model_validate(obj=created_supply)

    async def update_supply(
            self,
            session: AsyncSession,
            id: int,
            supply: SupplyCreateUpdateSchema,
    ) -> SupplySchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(supply.model_dump())
            .returning(self._collection)
        )

        updated_supply = await session.scalar(query)

        if not updated_supply:
            raise NotFound(_object=f"{self._type}", _id=id)

        return SupplySchema.model_validate(obj=updated_supply)

    async def delete_supply(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.supply where id = {id};"

        supply = await session.execute(text(query))