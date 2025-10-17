from functools import cached_property

from cryptography.hazmat.primitives import serialization
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    PRIVATE_KEY_PATH: str
    PUBLIC_KEY_PATH: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int
    REFRESH_TOKEN_LIFETIME_DAYS: int

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file="../../../.env",  # TODO: Вынести в отдельный env?
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
