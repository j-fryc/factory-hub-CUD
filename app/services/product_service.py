from fastapi import Depends
from pydantic_core import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.product_repository import get_product_repository
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductOut

from app.repositories.product_repository import ProductRepository
from app.services.abstract_service import AbstractService
from app.services.services_exceptions import DBException


class ProductService(AbstractService):
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    async def create(self, data: ProductCreate) -> ProductOut:
        try:
            serialized_data = data.model_dump()
            created_product = await self._repository.add(serialized_data)
            return ProductOut.model_validate(created_product)
        except ValidationError as e:
            raise e
        except SQLAlchemyError as e:
            raise DBException(e)

    async def update(self, product_id: str, data: ProductUpdate) -> ProductOut:
        try:
            serialized_data = data.model_dump()
            updated_product = await self._repository.update(product_id, serialized_data)
            return ProductOut.model_validate(updated_product)
        except ValidationError as e:
            raise e
        except SQLAlchemyError as e:
            raise DBException(e)

    async def delete(self, product_id: str) -> None:
        try:
            return await self._repository.delete(product_id)
        except SQLAlchemyError as e:
            raise DBException(e)


def get_product_service(repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repository)
