from sqlalchemy.ext.asyncio import AsyncSession

from src.application.controllers.base import BaseController
from src.domain.bet.schemas import BetInfo
from src.infrastructure.db.dbrepo import DBStorage
from src.infrastructure.db.models import Bet


class BetsController(BaseController):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def make_bet(self, bet_info: BetInfo):
        repo = DBStorage(Bet, self.session)
        return await repo.create(**bet_info.model_dump())

    async def get_bet(self):
        repo = DBStorage(Bet, self.session)


