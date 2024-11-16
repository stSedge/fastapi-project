from pydantic import BaseModel, ConfigDict
from datetime import date

class SellingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_supply: int
    id_seller: int
    id_user: int
    count: int
    cost: int
    discount: int
    final_cost: int
    data: date