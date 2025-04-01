from sqlmodel import Session

from app.repositories.abstrac_repository import AbstractRepository


class BaseRepository(AbstractRepository):
    def __init__(self, model, db_handler: Session):
        self.model = model
        self.db_handler = db_handler

    def delete(self, reference):
        pass

    def add(self, model):
        pass

    def update(self, reference):
        pass
