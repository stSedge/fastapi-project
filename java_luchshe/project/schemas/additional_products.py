from pydantic import BaseModel, ConfigDict

class AddProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    id_type: int