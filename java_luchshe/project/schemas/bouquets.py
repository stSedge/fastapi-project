from pydantic import BaseModel, ConfigDict, Field


class BouquetCreateUpdateSchema(BaseModel):
    name: str
    size: str | None = Field(default=None)


class BouquetSchema(BouquetCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_type: int
    