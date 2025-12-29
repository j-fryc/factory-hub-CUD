import asyncio

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic_core import ValidationError

from starlette.status import HTTP_207_MULTI_STATUS


from app.db_sync.db_synchronizer import DBSync, get_db_synchronizer
from app.db_sync.exceptions import SyncQueueException
from app.repositories.repositories_exceptions import NotFoundError, InvalidDataError
from app.schemas.product_schemas import ProductCreate, ProductUpdate
from app.schemas.product_type_schemas import ProductTypeUpdate, ProductTypeCreate
from app.cud_services.product_service import ProductService, get_product_service
from app.cud_services.product_type_service import ProductTypeService, get_product_type_service
from app.cud_services.services_exceptions import DBException
from app.utils import get_product_type_lock

router = APIRouter(prefix="/api/v1/cud")


@router.post("/products/")
async def create_product(
        product_data: ProductCreate,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        created_product = await product_service.create(product_data)
        json_compatible_data = jsonable_encoder(created_product)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, InvalidDataError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.patch("/products/{product_id}")
async def update_product(
        product_id: str,
        product_data: ProductUpdate,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        updated_product = await product_service.update(product_id, product_data)
        json_compatible_data = jsonable_encoder(updated_product)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, NotFoundError, InvalidDataError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/products/{product_id}")
async def delete_product(
        product_id: str,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        await product_service.delete(product_id)
        return Response(status_code=204)
    except (ValidationError, NotFoundError, InvalidDataError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/product-types/")
async def create_product_type(
        product_type_data: ProductTypeCreate,
        product_type_service: ProductTypeService = Depends(get_product_type_service),
        lock: asyncio.Lock = Depends(get_product_type_lock)
):
    async with lock:
        try:
            created_product_type = await product_type_service.create(product_type_data)
            json_compatible_data = jsonable_encoder(created_product_type)
            return JSONResponse(content=json_compatible_data)
        except (ValidationError, InvalidDataError) as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except DBException as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )


@router.patch("/product-types/{product_type_id}")
async def update_product_type(
        product_type_id: str,
        product_type_data: ProductTypeUpdate,
        product_type_service: ProductTypeService = Depends(get_product_type_service)
):
    try:
        updated_product = await product_type_service.update(product_type_id, product_type_data)
        json_compatible_data = jsonable_encoder(updated_product)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, NotFoundError, InvalidDataError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/product-types/{product_type_id}")
async def delete_product_type(
        product_type_id: str,
        product_type_service: ProductTypeService = Depends(get_product_type_service)
):
    try:
        await product_type_service.delete(product_type_id)
        return Response(status_code=204)
    except (ValidationError, NotFoundError, InvalidDataError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


sync_router = APIRouter(prefix="/api/v1")


@sync_router.get("/sync-db")
async def sync_db(
        db_sync_manager: DBSync = Depends(get_db_synchronizer),
):
    try:
        db_sync_manager.sync_db()
        json_compatible_data = jsonable_encoder(db_sync_manager.last_sync_result)
        return JSONResponse(content=json_compatible_data)
    except (DBException, SyncQueueException) as e:
        json_compatible_data = jsonable_encoder(db_sync_manager.last_sync_result)
        return JSONResponse(
            status_code=HTTP_207_MULTI_STATUS,
            content=json_compatible_data
        )
