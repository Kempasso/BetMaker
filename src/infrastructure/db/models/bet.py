from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import VARCHAR, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.database import Base

UUIDHex = VARCHAR(32)


class Bet(Base):
    __tablename__ = "bet"
    id: Mapped[UUIDHex] = mapped_column(UUIDHex, primary_key=True)
    event_id: Mapped[UUIDHex] = mapped_column(UUIDHex)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        onupdate=lambda: datetime.now(tz=timezone.utc)
    )

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = uuid4().hex
        super().__init__(**kwargs)
