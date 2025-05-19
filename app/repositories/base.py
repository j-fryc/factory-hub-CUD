from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.abstrac_repository import AbstractRepository

from sqlmodel import SQLModel

from app.repositories.repositories_exceptions import InvalidDataError, DatabaseOperationError, NotFoundError


class BaseRepository(AbstractRepository):
    def __init__(self, model, db_handler: AsyncSession):
        self._model = model
        self._db_handler = db_handler

    async def delete(self, reference: str) -> None:
        entity = await self._db_handler.get(self._model, reference)
        if entity is None:
            raise NotFoundError(reference)
        try:
            await self._db_handler.delete(entity)
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e))

    async def add(self, data) -> SQLModel:
        try:
            entity = self._model(**data)
            self._db_handler.add(entity)
            await self._db_handler.flush()
            await self._db_handler.refresh(entity)
            return entity
        except ValueError as e:
            raise InvalidDataError(str(e))
        except IntegrityError as e:
            raise InvalidDataError(str(e))
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e))

    async def update(self, reference: str, data) -> SQLModel:
        entity = await self._db_handler.get(self._model, reference)
        if entity is None:
            raise NotFoundError(reference)
        try:
            for attr, value in data.items():
                if value and hasattr(entity, attr):
                    setattr(entity, attr, value)
            await self._db_handler.flush()
            await self._db_handler.refresh(entity)
            return entity
        except ValueError as e:
            raise InvalidDataError(str(e))
        except IntegrityError as e:
            raise InvalidDataError(str(e))
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e))
