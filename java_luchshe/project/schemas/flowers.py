from pydantic import BaseModel, ConfigDict, Field


class FlowerCreateUpdateSchema(BaseModel):
    name: str

class FlowerSchema(FlowerCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_type: int