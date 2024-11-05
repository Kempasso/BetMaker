from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.controllers.base import BaseController
from src.application.mediators.kafka import KafkaBroker


class EventsController(BaseController):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.mediator = KafkaBroker()

    async def get_events(self):
        action = "events.get_events"
        return await self._make_request(action=action)

    async def _make_request(self, action):
        print("make request")
        return await self.mediator.remote_call(action=action)
