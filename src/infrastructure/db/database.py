from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
        "pk": "%(table_name)s_pkey"
    }
)
Base = declarative_base(metadata=metadata)


def get_session_maker(url) -> sessionmaker[AsyncSession]:
    engine = create_async_engine(
        url, pool_size=100, max_overflow=100, pool_timeout=60
    )

    session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=True
    )

    return session_factory
