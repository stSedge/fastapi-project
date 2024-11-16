from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    gender: str
    total_sum: int
    discount: Optional[int]