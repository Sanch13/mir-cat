from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../../.env", env_ignore_empty=True, extra="ignore"
    )
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True  # False для программного запуска
    LOG_LEVEL: str = "info"  # info для production, debug для разработки
    USE_COLORS: bool = True


server_settings = ServerSettings()
