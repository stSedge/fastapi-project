from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class SellerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    gender: str
    data_start: date
    data_end: Optional[date]