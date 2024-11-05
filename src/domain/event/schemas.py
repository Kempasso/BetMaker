from datetime import datetime
from typing import Literal

from pydantic import BaseModel, confloat, field_validator


class UpdateEvent(BaseModel):
    event_id: str
    status: Literal["win", "lose", "wait"]


class Event(BaseModel):
    id: str
    status: Literal["win", "lose", "wait"]
    coefficient: float
    end_date: datetime

    @field_validator('coefficient')
    def round_to_two_decimal(cls, value: float) -> float:
        return round(value, 2)
