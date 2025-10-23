from src.application.auth.exceptions import UnauthorizedError
from src.application.auth.services.auth_user_service import AuthenticateUserService
from src.application.exception_decorator import handle_db_errors
from src.domain.user.dtos import UserAuthInputDto
from src.infrastructure.services.jwt.jwt_service import JWTService


class AuthUserUseCase:
    def __init__(
        self,
        auth_service: AuthenticateUserService,
        jwt_service: JWTService,
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service

    @handle_db_errors
    async def execute(self, dto: UserAuthInputDto, meta: dict) -> dict:
        user_entity = await self.auth_service.authenticate_user(dto)

        if user_entity is None:
            raise UnauthorizedError

        access_token = await self.jwt_service.create_access_token(user_entity)
        refresh_token = await self.jwt_service.create_refresh_token(user_entity)
        expires_in = self.jwt_service.settings.ACCESS_TOKEN_LIFETIME_MINUTES * 60
        expires_in_refresh = self.jwt_service.settings.REFRESH_TOKEN_LIFETIME_DAYS * 24 * 3600

        dict_ = {
            "expires_in": expires_in,
            "expires_in_refresh": expires_in_refresh,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return dict_
