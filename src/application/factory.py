import asyncio
from contextlib import asynccontextmanager
from typing import Iterable, Callable, Coroutine

from fastapi import APIRouter, FastAPI

from src.application.mediators.kafka import event_update_listener


def create(
    *,
    base_router_path: str,
    routers: Iterable[APIRouter],
    startup_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    shutdown_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    **kwargs
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if startup_tasks:
            await asyncio.gather(*[task() for task in startup_tasks])
        event_listener = asyncio.create_task(event_update_listener())
        yield

        if shutdown_tasks:
            await asyncio.gather(*[task() for task in shutdown_tasks])
        event_listener.cancel()
    app = FastAPI(
        lifespan=lifespan, **kwargs
    )

    for router in routers:
        app.include_router(router, prefix=base_router_path)
    return app
