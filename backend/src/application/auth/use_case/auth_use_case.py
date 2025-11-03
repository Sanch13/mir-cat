from src.application.auth.exceptions import UnauthorizedError
from src.application.auth.services.auth_token_service import AuthTokenService
from src.application.auth.services.auth_user_service import AuthenticateUserService
from src.application.exception_decorator import handle_db_errors
from src.domain.user.dtos import UserAuthInputDto


class AuthUserUseCase:
    def __init__(
        self,
        auth_service: AuthenticateUserService,
        token_service: AuthTokenService,
    ):
        self.auth_service = auth_service
        self.token_service = token_service

    @handle_db_errors
    async def execute(self, dto: UserAuthInputDto, meta: dict) -> dict:
        user_entity = await self.auth_service.authenticate_user(dto)

        if user_entity is None:
            raise UnauthorizedError

        data, payload = await self.token_service.create_token_pair(str(user_entity.id.value))
        await self.token_service.save_refresh_token(payload)
        return data
