from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    username: str = "default"
    password: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="redis_",
        case_sensitive=False,
        env_file="../../../.env",  # TODO: Вынести в отдельный env?
        env_file_encoding="utf-8",
        extra="ignore",  # Игнорировать лишние поля
    )

    @property
    def redis_url(self) -> str:
        if self.username and self.password:
            return f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"
        elif self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        else:
            return f"redis://{self.host}:{self.port}/{self.db}"


redis_config = RedisSettings()
