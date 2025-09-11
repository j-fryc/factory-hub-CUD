from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.product_type_schemas import ProductTypeCreate, ProductTypeUpdate, ProductTypeOut

from app.repositories.product_type_repository import ProductTypeRepository, get_product_type_repository
from app.cud_services.abstract_service import AbstractService

from pydantic_core import ValidationError

from app.cud_services.services_exceptions import DBException


class ProductTypeService(AbstractService):
    def __init__(self, repository: ProductTypeRepository):
        self._repository = repository

    async def create(self, data: ProductTypeCreate) -> ProductTypeOut:
        try:
            serialized_data = data.model_dump()
            created_product = await self._repository.add(serialized_data)
            return ProductTypeOut.model_validate(created_product)
        except ValidationError as e:
            raise e
        except SQLAlchemyError as e:
            raise DBException(e)

    async def update(self, product_id: str, data: ProductTypeUpdate) -> ProductTypeOut:
        try:
            serialized_data = data.model_dump()
            updated_product = await self._repository.update(product_id, serialized_data)
            return ProductTypeOut.model_validate(updated_product)
        except ValidationError as e:
            raise e
        except SQLAlchemyError as e:
            raise DBException(e)

    async def delete(self, product_id: str) -> None:
        try:
            return await self._repository.delete(product_id)
        except SQLAlchemyError as e:
            raise DBException(e)

    async def get_all_data(self):
        try:
            updated_product = await self._repository.get_all_data()
            return ProductTypeOut.model_validate(updated_product)
        except ValidationError as e:
            raise e
        except SQLAlchemyError as e:
            raise DBException(e)


def get_product_type_service(repository: ProductTypeRepository = Depends(get_product_type_repository)) -> ProductTypeService:
    return ProductTypeService(repository=repository)
