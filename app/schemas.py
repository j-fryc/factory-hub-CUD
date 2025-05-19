from pydantic import BaseModel, Field, conint, confloat
from uuid import UUID
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Name of product")
    product_type_id: UUID = Field(..., description="ID of the product type (UUID)")
    quantity: conint(ge=0) = Field(..., description="How many products are available")
    price: confloat(gt=0) = Field(..., description="Price per product")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="New name of product")
    product_type: Optional[UUID] = Field(None, description="New product type ID")
    quantity: Optional[conint(ge=0)] = Field(None, description="Updated quantity")
    price: Optional[confloat(gt=0)] = Field(None, description="Updated price")
