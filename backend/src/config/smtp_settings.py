from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.glob_settings import ENV_FILE


class SMTPSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str

    model_config = SettingsConfigDict(
        env_prefix="smtp_",
        case_sensitive=False,
        env_file=str(ENV_FILE),  # TODO: Вынести в отдельный env?
        env_file_encoding="utf-8",
        extra="ignore",  # Игнорировать лишние поля
    )
