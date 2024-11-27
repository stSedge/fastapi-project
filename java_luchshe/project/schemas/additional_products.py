from pydantic import BaseModel, ConfigDict, Field


class AdditionalProductCreateUpdateSchema(BaseModel):
    name: str

class AdditionalProductSchema(AdditionalProductCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_type: int