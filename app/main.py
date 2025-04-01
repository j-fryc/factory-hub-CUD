from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.routers import router as cud_router
from app.db_handler.db_handler import Database


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
    db = Database(connection_string='sqlite:///app/data/foo.db')
    db.create_db_and_tables()
    app.state.db = db

app.include_router(cud_router)


