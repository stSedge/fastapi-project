from pydantic import BaseModel, ConfigDict

class CompoundBouquetsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_bouquets: int
    id_flower: int
    count: int