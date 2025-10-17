from src.apps.user.services.auth_user_service import AuthenticateUserService
from src.apps.user.services.jwt_service import JWTService
from src.domain.user.dtos import UserAuthInputDto


class AuthUserUseCase:
    def __init__(
        self,
        auth_service: AuthenticateUserService,
        jwt_service: JWTService,
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service

    async def execute(self, dto: UserAuthInputDto) -> dict:
        user_entity = await self.auth_service.authenticate_user(dto)

        if user_entity is None:
            return {"message": "Неверный логин или пароль"}

        access_token = await self.jwt_service.create_access_token(user_entity)
        refresh_token = await self.jwt_service.create_refresh_token(user_entity)

        return {
            "message": "Добро пожаловать в систему",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
