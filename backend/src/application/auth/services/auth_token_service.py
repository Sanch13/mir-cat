from fastapi import HTTPException

from src.application.interfaces import IRefreshTokenRepository
from src.infrastructure.services.jwt.jwt_service import JWTService


class AuthTokenService:
    """
    Бизнес-логика работы с токенами.
    Orchestrates между JWTService и Repository.
    """

    def __init__(
        self,
        jwt_service: JWTService,
        token_repository: IRefreshTokenRepository,
    ):
        self.jwt_service = jwt_service
        self.token_repository = token_repository

    async def create_token_pair(self, user_id: str) -> tuple:
        """Создает пару токенов"""

        access_token = await self.jwt_service.create_access_token(user_id)
        refresh_token, payload = await self.jwt_service.create_refresh_token(user_id)

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": self.jwt_service.settings.ACCESS_TOKEN_LIFETIME_MINUTES * 60,
        }

        return data, payload

    async def save_refresh_token(self, payload: dict) -> None:
        redis_ttl = self.jwt_service.settings.REFRESH_TOKEN_LIFETIME_DAYS * 86400
        await self.token_repository.save(payload, redis_ttl)

    async def verify_refresh_token(self, refresh_token: str | None) -> dict | None:
        return await self.jwt_service.verify_refresh_token(refresh_token)

    async def exists_refresh_token(self, user_id: str, jti: str):
        if not await self.token_repository.exists(user_id, jti):
            raise HTTPException(status_code=401, detail="токен отозван или не существует")

    async def delete_refresh_token(self, user_id: str, jti: str) -> None:
        await self.token_repository.delete(user_id, jti)
