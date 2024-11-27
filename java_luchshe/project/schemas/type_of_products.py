from pydantic import BaseModel, ConfigDict, Field


class TypeOfProductCreateUpdateSchema(BaseModel):
    type: str


class TypeOfProductSchema(TypeOfProductCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

