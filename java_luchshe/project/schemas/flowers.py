from pydantic import BaseModel, ConfigDict

class FlowerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    id_type: int