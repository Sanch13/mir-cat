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

    async def create_token_pair(self, user_entity) -> dict:
        """Создает пару токенов"""

        access_token = await self.jwt_service.create_access_token(user_entity)
        refresh_token, payload = await self.jwt_service.create_refresh_token(user_entity)

        redis_ttl = self.jwt_service.settings.REFRESH_TOKEN_LIFETIME_DAYS * 86400
        await self.token_repository.save(payload, redis_ttl)

        expires_in = self.jwt_service.settings.ACCESS_TOKEN_LIFETIME_MINUTES * 60

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": expires_in,
        }
