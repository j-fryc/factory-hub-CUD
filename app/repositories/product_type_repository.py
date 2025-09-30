from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_handler.async_db_handler import get_async_db_session
from app.models import ProductType, AggregateType
from app.repositories.base import BaseRepository
from app.repositories.repositories_exceptions import NotFoundError, DatabaseOperationError


class ProductTypeRepository(BaseRepository):
    def __init__(self, db_handler):
        super().__init__(ProductType, db_handler)

    async def delete(self, reference: str) -> None:
        entity = await self._db_handler.get(self._model, reference)
        if entity is None:
            raise NotFoundError(reference)
        try:
            for product in entity.products:
                self._add_sync_entry(entity=product, event_type=AggregateType.DELETE)
            await self._db_handler.delete(entity)
            self._add_sync_entry(entity=entity, event_type=AggregateType.DELETE)
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e


def get_product_type_repository(db_session: AsyncSession = Depends(get_async_db_session)) -> ProductTypeRepository:
    return ProductTypeRepository(db_handler=db_session)
