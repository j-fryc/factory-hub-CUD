from fastapi import Depends

from app.repositories.repositories_exceptions import DatabaseOperationError
from app.schemas.product_type_schemas import ProductTypeCreate, ProductTypeUpdate, ProductTypeOut

from app.repositories.product_type_repository import ProductTypeRepository, get_product_type_repository
from app.cud_services.abstract_service import AbstractService


from app.cud_services.services_exceptions import DBException


class ProductTypeService(AbstractService):
    def __init__(self, repository: ProductTypeRepository):
        self._repository = repository

    async def create(self, data: ProductTypeCreate) -> ProductTypeOut:
        try:
            serialized_data = data.model_dump()
            created_product = await self._repository.add(data=serialized_data)
            return ProductTypeOut.model_validate(created_product)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def update(self, product_id: str, data: ProductTypeUpdate) -> ProductTypeOut:
        try:
            serialized_data = data.model_dump()
            updated_product = await self._repository.update(reference=product_id, data=serialized_data)
            return ProductTypeOut.model_validate(updated_product)
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
            return ProductTypeOut.model_validate(updated_product)
        except DatabaseOperationError as e:
            raise DBException(e) from e


def get_product_type_service(repository: ProductTypeRepository = Depends(get_product_type_repository)) -> ProductTypeService:
    return ProductTypeService(repository=repository)
