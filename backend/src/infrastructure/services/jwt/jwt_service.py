import uuid
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException

from src.config.settings import Settings


class JWTService:
    def __init__(self, settings: Settings):
        self.settings = settings.jwt

    async def create_access_token(self, user_id: str) -> str:
        minutes = self.settings.ACCESS_TOKEN_LIFETIME_MINUTES
        now = datetime.now(UTC)

        exp = int((now + timedelta(minutes=minutes)).timestamp())
        iat = int(now.timestamp())
        jti = str(uuid.uuid4())

        payload = {
            "sub": user_id,
            "exp": exp,
            "iat": iat,
            "jti": jti,
            "type": "access",
        }
        secret_key = self.settings.private_key
        algorithm = self.settings.ALGORITHM
        access_token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
        return access_token

    async def create_refresh_token(self, user_id: str) -> tuple:
        days = self.settings.REFRESH_TOKEN_LIFETIME_DAYS
        now = datetime.now(UTC)

        exp = int((now + timedelta(days=days)).timestamp())
        iat = int(now.timestamp())
        jti = str(uuid.uuid4())

        payload = {
            "sub": user_id,
            "exp": exp,
            "iat": iat,
            "jti": jti,
            "type": "refresh",
        }

        secret_key = self.settings.private_key
        algorithm = self.settings.ALGORITHM
        refresh_token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
        return refresh_token, payload

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

    async def verify_refresh_token(self, refresh_token: str | None) -> dict | None:
        """
        Проверка refresh токена
        """
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token missing!!!")

        try:
            payload = jwt.decode(
                jwt=refresh_token,
                key=self.settings.public_key,
                algorithms=[self.settings.ALGORITHM],
            )
            return payload
        # TODO: Сделать отдельную ошибку
        except Exception:
            return None
