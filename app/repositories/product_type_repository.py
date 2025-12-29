import json

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_handler.async_db_handler import get_async_db_session
from app.models import ProductType, AggregateType
from app.repositories.base import BaseRepository
from app.repositories.repositories_exceptions import NotFoundError, DatabaseOperationError


class ProductTypeRepository(BaseRepository):
    def __init__(self, db_handler: AsyncSession):
        super().__init__(model=ProductType, db_handler=db_handler)

    async def delete(self, reference: str) -> None:
        entity = await self._db_handler.get(self._model, reference)
        if entity is None:
            raise NotFoundError(reference)
        try:
            for product in entity.products:
                await self._db_handler.delete(product)
                product.entity_version += 1
                self._add_sync_entry(
                    entity=json.loads(product.json()),
                    aggregate_type=product.__tablename__,
                    event_type=AggregateType.DELETE
                )
            await self._db_handler.delete(entity)
            entity.entity_version += 1
            self._add_sync_entry(
                entity=json.loads(entity.json()),
                aggregate_type=entity.__tablename__,
                event_type=AggregateType.DELETE
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e


def get_product_type_repository(db_session: AsyncSession = Depends(get_async_db_session)) -> ProductTypeRepository:
    return ProductTypeRepository(db_handler=db_session)
