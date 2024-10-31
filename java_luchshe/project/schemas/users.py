from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    gender: str
    total_sum: int
    discount: int