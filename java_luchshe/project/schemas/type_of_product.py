from pydantic import BaseModel, ConfigDict

class TypeOfProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str