from pydantic import BaseModel, ConfigDict

class CompoundBouquetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_bouquet: int
    id_flower: int
    count: int

