from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Request

from app.db_handler.base_db_handler import BaseDatabase
from app.db_session_handler.async_session_handler import AsyncDatabaseSession


class AsyncDatabase(BaseDatabase[AsyncEngine]):
    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(
            self._sql_url,
            pool_size=self._pool_size,
            max_overflow=self._max_overflow,
            pool_timeout=self._pool_timeout,
        )

    async def create_db_and_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_db_session(request: Request) -> AsyncSession:
    async with AsyncDatabaseSession(request.app.state.async_db_handler.db_engine) as session:
        yield session
