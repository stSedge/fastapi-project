from pydantic import BaseModel, ConfigDict, Field
from datetime import date

    
class SellerCreateUpdateSchema(BaseModel):
    name: str
    age: int
    gender: str
    data_start: date
    data_end: date | None = Field(default=None)

class SellerSchema(SellerCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int