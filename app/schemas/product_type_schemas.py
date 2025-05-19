from typing import Optional

from sqlmodel import SQLModel
from pydantic import ConfigDict
import uuid as uuid_pkg


class ProductTypeOut(SQLModel):
    id: uuid_pkg.UUID
    type_name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ProductTypeCreate(SQLModel):
    type_name: str
    description: str


class ProductTypeUpdate(SQLModel):
    type_name: Optional[str] = None
    description: Optional[str] = None
