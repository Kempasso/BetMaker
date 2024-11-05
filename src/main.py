from src.api.v1 import bet, event
from src.application.factory import create

app = create(
    base_router_path="/api",
    routers=(
        bet.router,
        event.router
    ),
    exception_handlers=None,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
    title="Core Bet service",
)
