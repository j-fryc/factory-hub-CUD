from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Request

from app.db_handler.session_hanlder import DatabaseSession


class Database:
    def __init__(self, connection_string: str, pool_size: int = 20, max_overflow: int = 0):
        self.sql_url = connection_string
        self._engine = create_async_engine(
            self.sql_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=30,
        )

    @property
    def db_engine(self):
        return self._engine

    async def create_db_and_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


async def get_db_session(request: Request) -> AsyncSession:
    async with DatabaseSession(request.app.state.db.db_engine) as session:
        yield session
