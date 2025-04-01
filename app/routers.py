from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db_handler.db_handler import get_db_session
from app.repositories.product_repository import ProductRepository

router = APIRouter(prefix="/api/v1/cud")


@router.get("/items/")
def test_db(db_session: Session = Depends(get_db_session)):
    hero_repository = ProductRepository(db_handler=db_session)
    # here will be implemented service
    return ''
