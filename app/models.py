from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship
import uuid as uuid_pkg
from sqlalchemy import Column, JSON
from datetime import datetime
from enum import Enum


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


class QueueStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"


class AggregateType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class OutboxEvent(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    aggregate_type: str = Field(..., description="Type of object that event concerns")
    aggregate_id: uuid_pkg.UUID = Field(..., description="ID of the entity associated with the event")
    event_type: AggregateType = Field(..., description="Type of event, ex. create")
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON), description="Payload of the event")
    created_at: datetime = Field(default_factory=lambda: datetime.now(), description="Datetime when event was created")
    processed_at: datetime | None = Field(default=None, description="Datetime when event was processed")
    status: QueueStatus = Field(..., description="Status of processing event")
