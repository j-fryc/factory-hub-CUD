from fastapi import Depends

from app.repositories.product_repository import get_product_repository
from app.repositories.repositories_exceptions import DatabaseOperationError
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductOut

from app.repositories.product_repository import ProductRepository
from app.cud_services.abstract_service import AbstractService
from app.cud_services.services_exceptions import DBException


class ProductService(AbstractService):
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    async def create(self, data: ProductCreate) -> ProductOut:
        try:
            serialized_data = data.model_dump()
            created_product = await self._repository.add(data=serialized_data)
            return ProductOut.model_validate(created_product)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def update(self, product_id: str, data: ProductUpdate) -> ProductOut:
        try:
            serialized_data = data.model_dump()
            updated_product = await self._repository.update(reference=product_id, data=serialized_data)
            return ProductOut.model_validate(updated_product)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def delete(self, product_id: str) -> None:
        try:
            return await self._repository.delete(reference=product_id)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def get_all_data(self):
        try:
            updated_product = await self._repository.get_all_data()
            return ProductOut.model_validate(updated_product)
        except DatabaseOperationError as e:
            raise DBException(e) from e


def get_product_service(repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repository)
