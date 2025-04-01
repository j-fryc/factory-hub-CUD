from sqlmodel import Session


class DatabaseSession:
    def __init__(self, engine):
        self._session = Session(engine)

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                self._session.commit()
            else:
                self._session.rollback()
        finally:
            self._session.close()
