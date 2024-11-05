from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.infrastructure.db.database import get_session_maker


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class PostgresConfig(BaseConfig):
    password: str = Field(validation_alias="POSTGRES_PASSWORD")
    user: str = Field(validation_alias="POSTGRES_USER")
    port: int = Field(validation_alias="POSTGRES_PORT")
    dbname: str = Field(validation_alias="POSTGRES_DB")
    host: str = Field(validation_alias="POSTGRES_HOST")

    @property
    def postgres_async_url(self) -> str:
        return (f"postgresql+asyncpg://"
                f"{self.user}:"
                f"{self.password}@"
                f"{self.host}:"
                f"{self.port}/"
                f"{self.dbname}")

    @property
    def postgres_sync_url(self) -> str:
        return (f"postgresql://{self.user}:"
                f"{self.password}@"
                f"{self.host}:"
                f"{self.port}/"
                f"{self.dbname}")


class KafkaConfig(BaseConfig):
    bootstrap_servers: str = Field(field="BOOTSTRAP_SERVERS")


class ServerConfig(BaseConfig):
    postgres: PostgresConfig = PostgresConfig()
    kafka: KafkaConfig = KafkaConfig()


class Settings:
    conf: ServerConfig = ServerConfig()
    session_factory: sessionmaker[AsyncSession]

    def setup(self):
        self.session_factory = get_session_maker(
            self.conf.postgres.postgres_async_url
        )
        return self


server = Settings().setup()
