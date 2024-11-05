from sqlalchemy.ext.asyncio import AsyncSession

from src.application import controllers
from src.config import server


class ServiceManager:
    session: AsyncSession
    bets: controllers.BetsController
    events: controllers.EventsController

    def __init__(self, session: AsyncSession = None):
        if session is None:
            self.session = server.session_factory()
        else:
            self.session = session

        self.bets = controllers.BetsController(self.session)
        self.events = controllers.EventsController(self.session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()


async def get_service_manager():
    print(1)
    async with server.session_factory() as session:
        print(2)
        manager = ServiceManager(session)
        print(3)
        try:
            yield manager
            await manager.commit()
        except Exception as ex:
            await manager.rollback()
            raise ex from ex
        finally:
            await manager.close()
