from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str

    model_config = SettingsConfigDict(
        env_prefix="smtp_",
        case_sensitive=False,
        env_file="../../../.env",  # TODO: Вынести в отдельный env?
        env_file_encoding="utf-8",
        extra="ignore",  # Игнорировать лишние поля
    )
