from typing import Optional

from sqlmodel import SQLModel
from pydantic import ConfigDict
import uuid as uuid_pkg

from app.schemas.product_type_schemas import ProductTypeOut


class ProductCreate(SQLModel):
    name: str
    quantity: int
    price: float
    product_type_id: uuid_pkg.UUID


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    product_type_id: Optional[uuid_pkg.UUID] = None


class ProductOut(SQLModel):
    id: uuid_pkg.UUID
    name: str
    quantity: int
    price: float
    product_type: ProductTypeOut

    model_config = ConfigDict(from_attributes=True)
