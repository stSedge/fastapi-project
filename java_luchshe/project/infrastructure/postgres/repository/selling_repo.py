from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.selling import SellingCreateUpdateSchema, SellingSchema
from project.infrastructure.postgres.models import Selling

from project.core.config import settings
from project.core.exceptions import NotFound


class SellingRepository:
    _collection: Type[Selling] = Selling
    _type: str = "Selling"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_selling(
        self,
        session: AsyncSession,
    ) -> list[SellingSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.selling;"

        sellings = await session.execute(text(query))

        return [SellingSchema.model_validate(obj=selling) for selling in sellings.mappings().all()]

    async def get_selling_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> SellingSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        selling = await session.scalar(query)

        if not selling:
            raise NotFound(_object=f"{self._type}", _id=id)

        return SellingSchema.model_validate(obj=selling)

    async def create_selling(
            self,
            session: AsyncSession,
            selling1: SellingCreateUpdateSchema,
    ) -> SellingSchema:
        query = (
            insert(self._collection)
            .values(selling1.model_dump())
            .returning(self._collection)
        )
        created_selling = await session.scalar(query)
        await session.commit()

        return SellingSchema.model_validate(obj=created_selling)

    async def update_selling(
            self,
            session: AsyncSession,
            id: int,
            selling: SellingCreateUpdateSchema,
    ) -> SellingSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(selling.model_dump())
            .returning(self._collection)
        )

        updated_selling = await session.scalar(query)
        if not updated_selling:
            raise NotFound(_object=f"{self._type}", _id=id)

        return SellingSchema.model_validate(obj=updated_selling)

    async def delete_selling(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.selling where id = {id};"

        selling = await session.execute(text(query))