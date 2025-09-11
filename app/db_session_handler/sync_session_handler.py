from sqlmodel import Session


class SyncDatabaseSession:
    def __init__(self, engine):
        self._engine = engine
        self._session = None

    def __enter__(self):
        self._session = Session(self._engine)
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
        self._session.close()
