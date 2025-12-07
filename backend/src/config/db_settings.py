from typing import ClassVar

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from src.config.glob_settings import ENV_FILE


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_ignore_empty=True, extra="ignore")
    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password"
    POSTGRES_DB: str = "test_database"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = -1
    POOL_PRE_PING: bool = True
    POOL_USE_LIFO: bool = True
    ECHO: bool = True
    ECHO_POOL: bool = True

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )

    @property
    def construct_sqlalchemy_url(self) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """
        uri = URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.POSTGRES_DB,
        )
        return uri.render_as_string(hide_password=False)

    @property
    def construct_sync_sqlalchemy_url(self) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """
        uri = URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.POSTGRES_DB,
        )
        return uri.render_as_string(hide_password=False)

    naming_convention: ClassVar[dict] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
