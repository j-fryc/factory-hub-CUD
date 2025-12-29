import asyncio

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.routers import router as cud_router, sync_router
from app.db_handler.async_db_handler import AsyncDatabase
from app.db_handler.sync_db_handler import SyncDatabase


app = FastAPI()

settings = get_settings()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="fastapi_session",
    max_age=3600,
)

@app.on_event("startup")
async def startup():
    async_db_handler = AsyncDatabase(
        connection_string=settings.db_async_connection_string
    )
    sync_db_handler = SyncDatabase(
        connection_string=settings.db_sync_connection_string
    )
    # await async_db_handler.create_db_and_tables()
    app.state.async_db_handler = async_db_handler
    app.state.sync_db_handler = sync_db_handler
    app.state.product_type_lock = asyncio.Lock()

app.include_router(cud_router)
app.include_router(sync_router)
