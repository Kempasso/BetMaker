from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.manager import get_service_manager, ServiceManager
from src.domain.bet.schemas import BetInfo, BetResponse

router = APIRouter(prefix="/v1")


@router.post("/bet")
async def make_bet(
    bet_info: BetInfo,
    manager: Annotated[
        ServiceManager,
        Depends(get_service_manager)
    ]
) -> BetResponse:
    bet = await manager.bets.make_bet(bet_info)
    return bet

#sudo docker compose -f compose.yaml core_backend up --build -d

@router.get("/bets")
async def get_filtered_bets(
    manager: Annotated[
        ServiceManager,
        Depends(get_service_manager)
    ]
) -> list[BetResponse]:

    bets = await manager.bets.get_bets()
    return bets
