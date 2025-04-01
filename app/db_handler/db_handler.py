from sqlmodel import SQLModel, create_engine
from fastapi import Request

from app.db_handler.session_hanlder import DatabaseSession


class Database:
    def __init__(self, connection_string: str, pool_size: int = 20, max_overflow: int = 0):
        self.sql_url = connection_string
        self.connect_args = {"check_same_thread": False}
        self._engine = create_engine(
            self.sql_url,
            connect_args=self.connect_args,
            pool_size=pool_size,
            max_overflow=max_overflow
        )

    @property
    def db_engine(self):
        return self._engine

    def create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self._engine)


def get_db_session(request: Request):
    with DatabaseSession(request.app.state.db.db_engine) as session:
        yield session
