from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.abstrac_repository import AbstractRepository


class BaseRepository(AbstractRepository):
    def __init__(self, model, db_handler: AsyncSession):
        self.model = model
        self.db_handler = db_handler

    async def delete(self, reference):
        pass

    async def add(self, model):
        pass

    async def update(self, reference):
        pass
