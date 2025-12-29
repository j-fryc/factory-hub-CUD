from typing import Optional

from pydantic import ConfigDict, BaseModel
import uuid as uuid_pkg

from app.schemas.product_type_schemas import ProductTypeOut


class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: float
    product_type_id: uuid_pkg.UUID


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    product_type_id: Optional[uuid_pkg.UUID] = None


class ProductOut(BaseModel):
    id: uuid_pkg.UUID
    name: str
    quantity: int
    price: float
    product_type: ProductTypeOut

    model_config = ConfigDict(from_attributes=True)
