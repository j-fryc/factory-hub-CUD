from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine


EngineType = TypeVar('EngineType', bound=Engine | AsyncEngine)


class BaseDatabase(ABC, Generic[EngineType]):
    def __init__(self, connection_string: str, pool_size: int = 20, max_overflow: int = 0):
        self._sql_url = connection_string
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._pool_timeout = 30
        self._engine = self._create_engine()

    @abstractmethod
    def _create_engine(self) -> EngineType:
        pass

    @property
    def db_engine(self) -> EngineType:
        return self._engine
