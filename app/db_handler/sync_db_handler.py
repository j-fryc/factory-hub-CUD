from sqlalchemy import Engine
from sqlmodel import create_engine, Session
from fastapi import Request

from app.db_handler.base_db_handler import BaseDatabase
from app.db_session_handler.sync_session_handler import SyncDatabaseSession


class SyncDatabase(BaseDatabase[Engine]):
    def _create_engine(self) -> Engine:
        return create_engine(
            self._sql_url,
            pool_size=self._pool_size,
            max_overflow=self._max_overflow,
            pool_timeout=self._pool_timeout,
        )


def get_sync_db_session(request: Request) -> Session:
    with SyncDatabaseSession(request.app.state.sync_db_handler.db_engine) as session:
        yield session
