from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.users import UserCreateUpdateSchema, UserSchema
from project.infrastructure.postgres.models import User

from project.core.config import settings
from project.core.exceptions import NotFound, UserAlreadyExists


class UserRepository:
    _collection: Type[User] = User
    _type : str = "User"

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:

        query = f"select * from {settings.POSTGRES_SCHEMA}.users;"

        users = await session.execute(text(query))

        return [UserSchema.model_validate(obj=user) for user in users.mappings().all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == id)
        )

        user = await session.scalar(query)

        if not user:
            raise NotFound(_object=f"{self._type}", _id=id)

        return UserSchema.model_validate(obj=user)

    async def create_user(
            self,
            session: AsyncSession,
            user1: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            insert(self._collection)
            .values(user1.model_dump())
            .returning(self._collection)
        )
        try:
            created_user = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise UserAlreadyExists(email=user1.email)

        return UserSchema.model_validate(obj=created_user)

    async def update_user(
            self,
            session: AsyncSession,
            id: int,
            user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == id)
            .values(user.model_dump())
            .returning(self._collection)
        )

        updated_user = await session.scalar(query)

        if not updated_user:
            raise NotFound(_object=f"{self._type}", _id=id)

        return UserSchema.model_validate(obj=updated_user)

    async def delete_user(
        self,
        session: AsyncSession,
        id: int
    ) -> None:
        query = f"delete from {settings.POSTGRES_SCHEMA}.users where id = {id};"

        user = await session.execute(text(query))

        if not user:
            raise NotFound(_object=f"{self._type}", _id=id)