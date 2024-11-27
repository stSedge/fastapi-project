from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete

from project.schemas.flowers import FlowerCreateUpdateSchema, FlowerSchema
from project.infrastructure.postgres.models import Flower

from project.core.config import settings
from project.core.exceptions import NotFound


class FlowerRepository:
    _collection: Type[Flower] = Flower
    _type: str = "Flower"

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

    async def get_flower_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> FlowerSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        flower = await session.scalar(query)

        if not flower:
            raise NotFound(_object=f"{self._type}", _id=id)

        return FlowerSchema.model_validate(obj=flower)

    async def create_flower(
            self,
            session: AsyncSession,
            flower1: FlowerCreateUpdateSchema,
    ) -> FlowerSchema:
        query = (
            insert(self._collection)
            .values(**flower1.model_dump(), id_type=1)
            .returning(self._collection)
        )
        created_flower = await session.scalar(query)
        await session.commit()

        return FlowerSchema.model_validate(obj=created_flower)

    async def update_flower(
            self,
            session: AsyncSession,
            id: int,
            flower: FlowerCreateUpdateSchema,
    ) -> FlowerSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(flower.model_dump())
            .returning(self._collection)
        )

        updated_flower = await session.scalar(query)

        if not updated_flower:
            raise NotFound(_object=f"{self._type}", _id=id)

        return FlowerSchema.model_validate(obj=updated_flower)

    async def delete_flower(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.flowers where id = {id};"

        flower = await session.execute(text(query))