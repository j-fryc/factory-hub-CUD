from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship
import uuid as uuid_pkg


class ProductType(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    type_name: str = Field(..., description="Name of the product type")
    description: str = Field(..., description="Description of the product type")
    products: List["Product"] = Relationship(
        back_populates="product_type",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Product(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str = Field(..., description="Name of the product")
    product_type_id: uuid_pkg.UUID = Field(
        foreign_key="producttype.id",
        nullable=False
    )
    product_type: Optional[ProductType] = Relationship(
        back_populates="products",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    quantity: int = Field(..., description="Quantity of products")
    price: float = Field(..., index=True, description="Price of single product")
