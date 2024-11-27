from pydantic import BaseModel, ConfigDict, Field


class UserCreateUpdateSchema(BaseModel):
    name: str
    age: int
    gender: str
    total_sum: int
    discount: int | None = Field(default=None)
    email: str
    password: str

class UserSchema(UserCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int