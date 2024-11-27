from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class SellingCreateUpdateSchema(BaseModel):
    id_supply: int
    id_seller: int
    id_user: int
    count: int
    cost: int
    discount: int
    final_cost: int
    data: date

class SellingSchema(SellingCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int