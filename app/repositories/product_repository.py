from app.models import Hero
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, db_handler):
        super().__init__(Hero, db_handler)
