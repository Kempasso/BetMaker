from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.manager import ServiceManager, get_service_manager
from src.domain.event.schemas import Event

router = APIRouter(prefix="/v1")


@router.get("/events")
async def all_events(
    manager: Annotated[
        ServiceManager,
        Depends(get_service_manager)
    ]
) -> list[Event]:
    print("here")
    events = await manager.events.get_events()
    return events
