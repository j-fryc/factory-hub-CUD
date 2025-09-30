from pydantic import ConfigDict
from sqlmodel import SQLModel
import uuid as uuid_pkg

from app.models import AggregateType


class OutboxEventDTO(SQLModel):
    id: uuid_pkg.UUID
    aggregate_type: str
    aggregate_id: uuid_pkg.UUID
    event_type: AggregateType
    payload: dict

    model_config = ConfigDict(from_attributes=True)