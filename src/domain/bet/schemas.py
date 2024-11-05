from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class BetInfo(BaseModel):
    event_id: str
    until: datetime
    status: Literal["win", "lose", "wait"]


class BetResponse(BetInfo):
    id: str
