from pydantic_settings import BaseSettings

from src.config.db_settings import DBSettings
from src.config.redis_settings import RedisSettings
from src.config.server_settings import ServerSettings
from src.config.smtp_settings import SMTPSettings


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    smtp: SMTPSettings = SMTPSettings()
    server: ServerSettings = ServerSettings()


settings = Settings()
