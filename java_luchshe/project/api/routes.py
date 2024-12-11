from fastapi import APIRouter, status, HTTPException, Depends

from project.core.exceptions import NotFound, UserAlreadyExists
from project.resource.auth import get_password_hash
from project.api.depends import database, user_repo, get_current_user, check_for_admin_access

from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.repository.seller_repo import SellerRepository
from project.infrastructure.postgres.repository.flower_repo import FlowerRepository
from project.infrastructure.postgres.repository.bouquet_repo import BouquetRepository
from project.infrastructure.postgres.repository.type_of_product_repo import TypeOfProductRepository
from project.infrastructure.postgres.repository.additional_product_repo import AdditionalProductRepository
from project.infrastructure.postgres.repository.supply_repo import SupplyRepository
from project.infrastructure.postgres.repository.selling_repo import SellingRepository
from project.infrastructure.postgres.repository.compound_bouquet_repo import CompoundBouquetRepository

from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.users import UserCreateUpdateSchema
from project.schemas.users import UserSchema
from project.schemas.sellers import SellerSchema
from project.schemas.sellers import SellerCreateUpdateSchema
from project.schemas.flowers import FlowerSchema
from project.schemas.flowers import FlowerCreateUpdateSchema
from project.schemas.bouquets import BouquetSchema
from project.schemas.bouquets import BouquetCreateUpdateSchema
from project.schemas.type_of_products import TypeOfProductCreateUpdateSchema
from project.schemas.type_of_products import TypeOfProductSchema
from project.schemas.additional_products import AdditionalProductCreateUpdateSchema
from project.schemas.additional_products import AdditionalProductSchema
from project.schemas.selling import SellingCreateUpdateSchema
from project.schemas.selling import SellingSchema
from project.schemas.supply import SupplyCreateUpdateSchema
from project.schemas.supply import SupplySchema
from project.schemas.compound_bouquet import CompoundBouquetSchema

router = APIRouter()

##############################################################################################################
# USERS

@router.get("/all_users",
            status_code=status.HTTP_200_OK,
            response_model=list[UserSchema])
async def get_all_users(
    current_user: UserSchema = Depends(get_current_user),
) -> list[UserSchema]:
    user_repo = UserRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_users = await user_repo.get_all_users(session=session)

    return all_users

@router.get("/user/{id}",
            status_code=status.HTTP_200_OK,
            response_model=UserSchema)
async def get_user_by_id(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await user_repo.check_connection(session=session)
            user = await user_repo.get_user_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user

@router.post("/create_user",
             status_code=status.HTTP_201_CREATED,
             response_model=UserSchema)
async def create_user(
    user_dto: UserCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    try:
        async with database.session() as session:
            user_dto.password = get_password_hash(password=user_dto.password)
            if user_dto.is_admin:
                check_for_admin_access(user=current_user)
            new_user = await user_repo.create_user(session=session, user1=user_dto)
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_user


@router.put(
    "/update_user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def update_user(
    id: int,
    user_dto: UserCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            user_dto.password = get_password_hash(password=user_dto.password)
            updated_user = await user_repo.update_user(
                session=session,
                id=id,
                user=user_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_user

@router.delete("/delete_user/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_user(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    user_repo = UserRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await user_repo.check_connection(session=session)
            user = await user_repo.delete_user(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user

##############################################################################################################
# SELLERS

@router.get("/all_sellers",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)],
            response_model=list[SellerSchema])
async def get_all_sellers() -> list[SellerSchema]:
    seller_repo = SellerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await seller_repo.check_connection(session=session)
        all_sellers = await seller_repo.get_all_sellers(session=session)

    return all_sellers


@router.get("/seller/{id}",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)],
            response_model=SellerSchema)
async def get_seller_by_id(id :int) -> SellerSchema:
    seller_repo = SellerRepository()
    database = PostgresDatabase()

    try:
        async with database.session() as session:
            await seller_repo.check_connection(session=session)
            seller = await seller_repo.get_seller_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return seller

@router.post("/create_seller",
             status_code=status.HTTP_201_CREATED,
             response_model=SellerSchema)
async def create_seller(
    seller_dto: SellerCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> SellerSchema:
    seller_repo = SellerRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_seller = await seller_repo.create_seller(session=session, seller1=seller_dto)

    return new_seller


@router.put(
    "/update_seller/{seller_id}",
    status_code=status.HTTP_200_OK,
    response_model=SellerSchema,
)
async def update_seller(
    id: int,
    seller_dto: SellerCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> SellerSchema:
    seller_repo = SellerRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_seller = await seller_repo.update_seller(
                session=session,
                id=id,
                seller=seller_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_seller


@router.delete("/delete_seller/{id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_seller(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    seller_repo = SellerRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await seller_repo.check_connection(session=session)
            seller = await seller_repo.delete_seller(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return seller


##############################################################################################################
# FLOWERS

@router.get("/all_flowers",
            status_code=status.HTTP_200_OK,
            response_model=list[FlowerSchema])
async def get_all_flowers() -> list[FlowerSchema]:
    flower_repo = FlowerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await flower_repo.check_connection(session=session)
        all_flowers = await flower_repo.get_all_flowers(session=session)

    return all_flowers


@router.get("/flower/{id}",
            status_code=status.HTTP_200_OK,
            response_model=FlowerSchema)
async def get_flower_by_id(id :int) -> FlowerSchema:
    flower_repo = FlowerRepository()
    database = PostgresDatabase()

    try:
        async with database.session() as session:
            await flower_repo.check_connection(session=session)
            flower = await flower_repo.get_flower_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return flower

@router.post("/create_flower",
             status_code=status.HTTP_201_CREATED,
             response_model=FlowerSchema)
async def create_flower(
    flower_dto: FlowerCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> FlowerSchema:
    flower_repo = FlowerRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_flower = await flower_repo.create_flower(session=session, flower1=flower_dto)

    return new_flower


@router.put(
    "/update_flower/{flower_id}",
    status_code=status.HTTP_200_OK,
    response_model=FlowerSchema
)
async def update_flower(
    id: int,
    flower_dto: FlowerCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> FlowerSchema:
    flower_repo = FlowerRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_flower = await flower_repo.update_flower(
                session=session,
                id=id,
                flower=flower_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_flower


@router.delete("/delete_flower/{id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_flower(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    flower_repo = FlowerRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await flower_repo.check_connection(session=session)
            flower = await flower_repo.delete_flower(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return flower

##############################################################################################################
# BOUQUETS

@router.get("/all_bouquets",
            status_code=status.HTTP_200_OK,
            response_model=list[BouquetSchema])
async def get_all_bouquets() -> list[BouquetSchema]:
    bouquet_repo = BouquetRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await bouquet_repo.check_connection(session=session)
        all_bouquets = await bouquet_repo.get_all_bouquets(session=session)

    return all_bouquets


@router.get("/bouquet/{id}",
            status_code=status.HTTP_200_OK,
            response_model=BouquetSchema)
async def get_bouquet_by_id(id :int) -> BouquetSchema:
    bouquet_repo = BouquetRepository()
    database = PostgresDatabase()

    try:
        async with database.session() as session:
            await bouquet_repo.check_connection(session=session)
            bouquet = await bouquet_repo.get_bouquet_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bouquet

@router.post("/create_bouquet", response_model=BouquetSchema)
async def create_bouquet(
    bouquet_dto: BouquetCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> BouquetSchema:
    bouquet_repo = BouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_bouquet = await bouquet_repo.create_bouquet(session=session, bouquet1=bouquet_dto)

    return new_bouquet


@router.put(
    "/update_bouquet/{bouquet_id}",
    status_code=status.HTTP_200_OK,
    response_model=BouquetSchema
)
async def update_bouquet(
    id: int,
    bouquet_dto: BouquetCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> BouquetSchema:
    bouquet_repo = BouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_bouquet = await bouquet_repo.update_bouquet(
                session=session,
                id=id,
                bouquet=bouquet_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_bouquet


@router.delete("/delete_bouquet/{id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_bouquet(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    bouquet_repo = BouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await bouquet_repo.check_connection(session=session)
            bouquet = await bouquet_repo.delete_bouquet(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bouquet

##############################################################################################################
# TYPEOFRRODUCTS

@router.get("/all_type_of_products",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)],
            response_model=list[TypeOfProductSchema])
async def get_all_type_of_products() -> list[TypeOfProductSchema]:
    type_of_product_repo = TypeOfProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await type_of_product_repo.check_connection(session=session)
        all_type_of_products = await type_of_product_repo.get_all_type_of_products(session=session)

    return all_type_of_products


@router.get("/type_of_product/{id}",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)],
            response_model=TypeOfProductSchema)
async def get_type_of_product_by_id(id :int) -> TypeOfProductSchema:
    type_of_product_repo = TypeOfProductRepository()
    database = PostgresDatabase()

    try:
        async with database.session() as session:
            await type_of_product_repo.check_connection(session=session)
            type_of_product = await type_of_product_repo.get_type_of_product_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return type_of_product

@router.post("/create_type_of_product",
             status_code=status.HTTP_201_CREATED,
             response_model=TypeOfProductSchema)
async def create_type_of_product(
    type_of_product_dto: TypeOfProductCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> TypeOfProductSchema:
    type_of_product_repo = TypeOfProductRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_type_of_product = await type_of_product_repo.create_type_of_product(session=session, type_of_product1=type_of_product_dto)

    return new_type_of_product


@router.put(
    "/update_type_of_product/{type_of_product_id}",
    status_code=status.HTTP_200_OK,
    response_model=TypeOfProductSchema,
)
async def update_type_of_product(
    id: int,
    type_of_product_dto: TypeOfProductCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> TypeOfProductSchema:
    type_of_product_repo = TypeOfProductRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_type_of_product = await type_of_product_repo.update_type_of_product(
                session=session,
                id=id,
                type_of_product=type_of_product_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_type_of_product


@router.delete("/delete_type_of_product/{id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_type_of_product(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    type_of_product_repo = TypeOfProductRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await type_of_product_repo.check_connection(session=session)
            type_of_product = await type_of_product_repo.delete_type_of_product(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return type_of_product

##############################################################################################################
# ADDITIONALRRODUCTS

@router.get("/all_additional_products",
            status_code=status.HTTP_200_OK,
            response_model=list[AdditionalProductSchema])
async def get_all_additional_products() -> list[AdditionalProductSchema]:
    additional_product_repo = AdditionalProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await additional_product_repo.check_connection(session=session)
        all_additional_products = await additional_product_repo.get_all_additional_products(session=session)

    return all_additional_products


@router.get("/additional_product/{id}",
            status_code=status.HTTP_200_OK,
            response_model=AdditionalProductSchema)
async def get_additional_product_by_id(id :int) -> AdditionalProductSchema:
    additional_product_repo = AdditionalProductRepository()
    database = PostgresDatabase()

    try:
        async with database.session() as session:
            await additional_product_repo.check_connection(session=session)
            additional_product = await additional_product_repo.get_additional_product_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return additional_product

@router.post("/create_additional_product",
             status_code=status.HTTP_201_CREATED,
             response_model=AdditionalProductSchema)
async def create_additional_product(
    additional_product_dto: AdditionalProductCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> AdditionalProductSchema:
    additional_product_repo = AdditionalProductRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_additional_product = await additional_product_repo.create_additional_product(session=session, additional_product1=additional_product_dto)

    return new_additional_product


@router.put(
    "/update_additional_product/{additional_product_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdditionalProductSchema,
)
async def update_additional_product(
    id: int,
    additional_product_dto: AdditionalProductCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> AdditionalProductSchema:
    additional_product_repo = AdditionalProductRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_additional_product = await additional_product_repo.update_additional_product(
                session=session,
                id=id,
                additional_product=additional_product_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_additional_product


@router.delete("/delete_additional_product/{id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_additional_product(
        id :int,
        current_user: UserSchema = Depends(get_current_user),
) -> None:
    additional_product_repo = AdditionalProductRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await additional_product_repo.check_connection(session=session)
            additional_product = await additional_product_repo.delete_additional_product(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return additional_product

##############################################################################################################
# SELLING

@router.get("/all_selling",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)],
            response_model=list[SellingSchema])
async def get_all_selling(
        current_user: UserSchema = Depends(get_current_user)
) -> list[SellingSchema]:
    selling_repo = SellingRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        await selling_repo.check_connection(session=session)
        all_selling = await selling_repo.get_all_selling(session=session)

    return all_selling

@router.get("/selling/{id}",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)],
            response_model=SellingSchema)
async def get_selling_by_id(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> SellingSchema:
    selling_repo = SellingRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await selling_repo.check_connection(session=session)
            selling = await selling_repo.get_selling_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return selling

@router.post("/create_selling",
             status_code=status.HTTP_201_CREATED,
             response_model=SellingSchema)
async def create_selling(
    selling_dto: SellingCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> SellingSchema:
    selling_repo = SellingRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_selling = await selling_repo.create_selling(session=session, selling1=selling_dto)

    return new_selling


@router.put(
    "/update_selling/{selling_id}",
    status_code=status.HTTP_200_OK,
    response_model=SellingSchema
)
async def update_selling(
    id: int,
    selling_dto: SellingCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> SellingSchema:
    selling_repo = SellingRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_selling = await selling_repo.update_selling(
                session=session,
                id=id,
                selling=selling_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_selling

@router.delete("/delete_selling/{selling_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_selling(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    selling_repo = SellingRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await selling_repo.check_connection(session=session)
            selling = await selling_repo.delete_selling(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return selling


##############################################################################################################
# SUPPLY

@router.get("/all_supply",
            status_code=status.HTTP_200_OK,
            response_model=list[SupplySchema])
async def get_all_supply(
    current_user: UserSchema = Depends(get_current_user),
) -> list[SupplySchema]:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        await supply_repo.check_connection(session=session)
        all_supply = await supply_repo.get_all_supply(session=session)

    return all_supply

@router.get("/supply/{id}",
            status_code=status.HTTP_200_OK,
            response_model=SupplySchema)
async def get_supply_by_id(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> SupplySchema:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await supply_repo.check_connection(session=session)
            supply = await supply_repo.get_supply_by_id(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return supply

@router.post("/create_supply",
             status_code=status.HTTP_201_CREATED,
             response_model=SupplySchema)
async def create_supply(
    supply_dto: SupplyCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> SupplySchema:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_supply = await supply_repo.create_supply(session=session, supply1=supply_dto)

    return new_supply


@router.put(
    "/update_supply/{supply_id}",
    status_code=status.HTTP_200_OK,
    response_model=SupplySchema
)
async def update_supply(
    id: int,
    supply_dto: SupplyCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> SupplySchema:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_supply = await supply_repo.update_supply(
                session=session,
                id=id,
                supply=supply_dto
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_supply

@router.delete("/delete_supply/{supply_id}",
               status_code=status.HTTP_204_NO_CONTENT
              )
async def delete_supply(
    id :int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await supply_repo.check_connection(session=session)
            supply = await supply_repo.delete_supply(session=session, id=id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return supply

##############################################################################################################
# COMPOUND_BOUQUET

@router.get("/all_compound_bouquets",
            status_code=status.HTTP_200_OK,
            response_model=list[CompoundBouquetSchema])
async def get_all_compound_bouquets(
    current_user: UserSchema = Depends(get_current_user),
) -> list[CompoundBouquetSchema]:
    compound_bouquet_repo = CompoundBouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        await compound_bouquet_repo.check_connection(session=session)
        all_compound_bouquets = await compound_bouquet_repo.get_all_compound_bouquets(session=session)

    return all_compound_bouquets

@router.get("/compound_bouquet/{id_bouquet}/{id_flower}",
            status_code=status.HTTP_200_OK,
            response_model=CompoundBouquetSchema)
async def get_compound_bouquet_by_id(
    id_bouquet :int,
    id_flower : int,
    current_user: UserSchema = Depends(get_current_user),
) -> CompoundBouquetSchema:
    compound_bouquet_repo = CompoundBouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await compound_bouquet_repo.check_connection(session=session)
            compound_bouquet = await compound_bouquet_repo.get_compound_bouquet_by_id(session=session, id_bouquet=id_bouquet, id_flower=id_flower)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return compound_bouquet

@router.post("/create_compound_bouquet",
             status_code=status.HTTP_201_CREATED,
             response_model=CompoundBouquetSchema)
async def create_compound_bouquet(
    compound_bouquet_dto: CompoundBouquetSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> CompoundBouquetSchema:
    compound_bouquet_repo = CompoundBouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_compound_bouquet = await compound_bouquet_repo.create_compound_bouquet(session=session, compound_bouquet1=compound_bouquet_dto)

    return new_compound_bouquet


@router.put(
    "/update_compound_bouquet/{bouquet_id}/{flower_id}",
    status_code=status.HTTP_200_OK,
    response_model=CompoundBouquetSchema
)
async def update_compound_bouquet(
    id_bouquet :int,
    id_flower : int,
    count: int,
    current_user: UserSchema = Depends(get_current_user),
) -> CompoundBouquetSchema:
    compound_bouquet_repo = CompoundBouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_compound_bouquet = await compound_bouquet_repo.update_compound_bouquet(
                session=session,
                id_bouquet=id_bouquet,
                id_flower=id_flower,
                count=count
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_compound_bouquet

@router.delete("/delete_compound_bouquet/{bouquet_id}/{flower_id}",
               status_code=status.HTTP_204_NO_CONTENT
              )
async def delete_compound_bouquet(
    id_bouquet :int,
    id_flower : int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    compound_bouquet_repo = CompoundBouquetRepository()
    database = PostgresDatabase()
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            await compound_bouquet_repo.check_connection(session=session)
            compound_bouquet = await compound_bouquet_repo.delete_compound_bouquet(session=session, id_bouquet=id_bouquet, id_flower=id_flower)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return compound_bouquet
