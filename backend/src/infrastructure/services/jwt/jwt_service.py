import uuid
from datetime import UTC, datetime, timedelta

import jwt
from redis.asyncio import Redis as AsyncRedis

from src.config.settings import Settings
from src.domain.user.entity import UserEntity


class JWTService:
    def __init__(self, settings: Settings, redis_client: AsyncRedis):
        self.settings = settings.jwt
        self.redis_client = redis_client

    async def create_access_token(self, user_entity: UserEntity) -> str:
        minutes = self.settings.ACCESS_TOKEN_LIFETIME_MINUTES
        now = datetime.now(UTC)
        exp = int((now + timedelta(minutes=minutes)).timestamp())
        iat = int(now.timestamp())

        payload = {
            "sub": str(user_entity.id.value),
            "exp": exp,
            "iat": iat,
            "jti": str(uuid.uuid4()),
            "type": "access",
        }
        secret_key = self.settings.private_key
        algorithm = self.settings.ALGORITHM
        access_token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
        return access_token

    async def create_refresh_token(self, user_entity: UserEntity) -> str:
        days = self.settings.REFRESH_TOKEN_LIFETIME_DAYS
        now = datetime.now(UTC)
        exp = int((now + timedelta(days=days)).timestamp())
        iat = int(now.timestamp())

        payload = {
            "sub": str(user_entity.id.value),
            "exp": exp,
            "iat": iat,
            "jti": str(uuid.uuid4()),
            "type": "refresh",
        }

        secret_key = self.settings.private_key
        algorithm = self.settings.ALGORITHM
        refresh_token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
        return refresh_token

    async def verify_access_token(self, token: str) -> dict | None:
        """Проверка access token"""
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.settings.public_key,
                algorithms=self.settings.ALGORITHM,
            )
            return payload
        # TODO: Сделать отдельную ошибку
        except Exception:
            return None
