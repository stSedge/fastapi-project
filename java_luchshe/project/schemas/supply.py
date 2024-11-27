from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class SupplyCreateUpdateSchema(BaseModel):
    id_type: int
    id_product: int
    count: int
    cost: int
    id_seller: int
    data: date

class SupplySchema(SupplyCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int