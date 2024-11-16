from pydantic import BaseModel, ConfigDict
from datetime import date

class SupplySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_type: int
    id_product: int
    count: int
    cost: int
    id_seller: int
    data: date