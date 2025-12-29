import json
from typing import List, Type

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

from app.repositories.abstrac_repository import AbstractRepository
from app.models import OutboxEvent, AggregateType, QueueStatus
from app.repositories.repositories_exceptions import InvalidDataError, DatabaseOperationError, NotFoundError


class BaseRepository(AbstractRepository):
    def __init__(self, model: Type[SQLModel], db_handler: AsyncSession):
        self._model = model
        self._db_handler = db_handler
        self._sync_model = OutboxEvent

    async def delete(self, reference: str) -> None:
        entity = await self._db_handler.get(self._model, reference)
        if entity is None:
            raise NotFoundError(reference)
        try:
            await self._db_handler.delete(entity)
            entity.entity_version += 1
            self._add_sync_entry(
                entity=json.loads(entity.json()),
                aggregate_type=entity.__tablename__,
                event_type=AggregateType.DELETE
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e

    async def add(self, data: dict) -> SQLModel:
        try:
            entity = self._model(**data)
            self._db_handler.add(entity)
            self._add_sync_entry(
                entity=json.loads(entity.json()),
                aggregate_type=entity.__tablename__,
                event_type=AggregateType.CREATE
            )
            await self._db_handler.flush()
            await self._db_handler.refresh(entity)
            return entity
        except ValueError as e:
            raise InvalidDataError(str(e)) from e
        except IntegrityError as e:
            raise InvalidDataError(str(e)) from e
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e

    async def update(self, reference: str, data: dict) -> SQLModel:
        entity = await self._db_handler.get(self._model, reference)
        if entity is None:
            raise NotFoundError(reference)
        try:
            for attr, value in data.items():
                if value and hasattr(entity, attr):
                    setattr(entity, attr, value)
            entity.entity_version += 1
            self._add_sync_entry(
                entity=json.loads(entity.json()),
                aggregate_type=entity.__tablename__,
                event_type=AggregateType.UPDATE
            )
            await self._db_handler.flush()
            await self._db_handler.refresh(entity)
            return entity
        except ValueError as e:
            raise InvalidDataError(str(e)) from e
        except IntegrityError as e:
            raise InvalidDataError(str(e)) from e
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e

    async def get_all_data(self) -> List[SQLModel]:
        try:
            result = await self._db_handler.exec(select(self._model))
            entities = result.all()
            if not entities:
                raise NotFoundError()
            return list(entities)
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e

    def _add_sync_entry(self, entity: dict, aggregate_type: str, event_type: AggregateType) -> None:
        sync_entity = self._sync_model(
            aggregate_type=aggregate_type,
            event_type=event_type,
            payload=entity,
            status=QueueStatus.PENDING
        )
        self._db_handler.add(sync_entity)
