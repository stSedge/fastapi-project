from fastapi import APIRouter

from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.repository.seller_repo import SellerRepository
from project.infrastructure.postgres.repository.flower_repo import FlowerRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.users import UserSchema
from project.schemas.sellers import SellerSchema
from project.schemas.flowers import FlowerSchema


router = APIRouter()


@router.get("/all_users", response_model=list[UserSchema])
async def get_all_users() -> list[UserSchema]:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_users = await user_repo.get_all_users(session=session)

    return all_users


@router.get("/all_sellers", response_model=list[SellerSchema])
async def get_all_sellers() -> list[SellerSchema]:
    seller_repo = SellerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await seller_repo.check_connection(session=session)
        all_sellers = await seller_repo.get_all_sellers(session=session)

    return all_sellers


@router.get("/all_flowers", response_model=list[FlowerSchema])
async def get_all_flowers() -> list[FlowerSchema]:
    flower_repo = FlowerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await flower_repo.check_connection(session=session)
        all_flowers = await flower_repo.get_all_flowers(session=session)

    return all_flowers