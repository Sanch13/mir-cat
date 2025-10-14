from src.apps.user.services.auth_user_service import AuthenticateUserService
from src.domain.user.dtos import UserAuthInputDto


class AuthUserUseCase:
    def __init__(self, auth_service: AuthenticateUserService):
        self.auth_service = auth_service

    async def execute(self, dto: UserAuthInputDto) -> dict:
        return await self.auth_service.authenticate_user(dto)
