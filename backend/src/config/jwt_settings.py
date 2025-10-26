from functools import cached_property

from cryptography.hazmat.primitives import serialization
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.glob_settings import ENV_FILE


class JWTSettings(BaseSettings):
    PRIVATE_KEY_PATH: str = "test_path"
    PUBLIC_KEY_PATH: str = "test_path"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 30
    REFRESH_TOKEN_LIFETIME_DAYS: int = 14

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=str(ENV_FILE),  # TODO: Вынести в отдельный env?
        env_file_encoding="utf-8",
        extra="ignore",  # Игнорировать лишние поля
    )

    @cached_property
    def private_key(self):
        with open(self.PRIVATE_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
            return private_key

    @cached_property
    def public_key(self):
        with open(self.PUBLIC_KEY_PATH, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
            )
            return public_key
