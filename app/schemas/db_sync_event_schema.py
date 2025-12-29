from typing import Union

from pydantic import ConfigDict, BaseModel
import uuid as uuid_pkg

from app.models import AggregateType


class OutboxEventEntity(BaseModel):
    id: uuid_pkg.UUID
    entity_version: int
    name: str


class ProductTypeEvent(OutboxEventEntity):
    description: str


class ProductEvent(OutboxEventEntity):
    product_type_id: uuid_pkg.UUID
    quantity: int
    price: float


class OutboxEventDTO(BaseModel):
    event_type: AggregateType
    payload: Union[ProductEvent, ProductTypeEvent]

    model_config = ConfigDict(from_attributes=True)
