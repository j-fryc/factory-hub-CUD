from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncDatabaseSession:
    def __init__(self, engine):
        self._engine = engine
        self._session = None

    async def __aenter__(self):
        self._session = AsyncSession(self._engine)
        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()
        await self._session.close()