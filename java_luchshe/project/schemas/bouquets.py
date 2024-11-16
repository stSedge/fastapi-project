from pydantic import BaseModel, ConfigDict
from typing import Optional

class BouquetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    id_type: int
    size: Optional[str]