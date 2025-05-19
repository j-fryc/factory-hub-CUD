from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_handler.db_handler import get_db_session
from app.models import ProductType
from app.repositories.base import BaseRepository


class ProductTypeRepository(BaseRepository):
    def __init__(self, db_handler):
        super().__init__(ProductType, db_handler)


def get_product_type_repository(db_session: AsyncSession = Depends(get_db_session)) -> ProductTypeRepository:
    return ProductTypeRepository(db_handler=db_session)
