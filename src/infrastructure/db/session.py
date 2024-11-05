from contextlib import asynccontextmanager

from src.config import server


@asynccontextmanager
async def make_session():
    async with server.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as ex:
            await session.rollback()
