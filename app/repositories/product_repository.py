from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_handler.db_handler import get_db_session
from app.models import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, db_handler):
        super().__init__(Product, db_handler)


def get_product_repository(db_session: AsyncSession = Depends(get_db_session)) -> ProductRepository:
    return ProductRepository(db_handler=db_session)
