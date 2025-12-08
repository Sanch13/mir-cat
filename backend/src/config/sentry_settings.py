from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.glob_settings import ENV_FILE


class SentrySettings(BaseSettings):
    dsn: str

    model_config = SettingsConfigDict(
        env_prefix="sentry_",
        case_sensitive=False,
        env_file=str(ENV_FILE),  # TODO: Вынести в отдельный env?
        env_file_encoding="utf-8",
        extra="ignore",
    )
