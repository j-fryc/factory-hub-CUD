from typing import Optional

from pydantic import ConfigDict, BaseModel
import uuid as uuid_pkg


class ProductTypeOut(BaseModel):
    id: uuid_pkg.UUID
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ProductTypeCreate(BaseModel):
    name: str
    description: str


class ProductTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
