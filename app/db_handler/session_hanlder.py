from sqlmodel.ext.asyncio.session import AsyncSession


class DatabaseSession:
    def __init__(self, engine):
        self._session = AsyncSession(engine)

    async def __aenter__(self):
        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
