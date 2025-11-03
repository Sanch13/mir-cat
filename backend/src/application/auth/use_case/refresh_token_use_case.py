from src.application.auth.services.auth_token_service import AuthTokenService


class RefreshTokenUseCase:
    def __init__(
        self,
        token_service: AuthTokenService,
    ):
        self.token_service = token_service

    async def execute(self, refresh_token: str | None) -> dict:
        payload = await self.token_service.verify_refresh_token(refresh_token)

        user_id = payload.get("sub")
        jti = payload.get("jti")

        print(f"-----------{user_id}--------------{jti}")
        await self.token_service.exists_refresh_token(user_id=user_id, jti=jti)
        await self.token_service.delete_refresh_token(user_id=user_id, jti=jti)

        data, payload = await self.token_service.create_token_pair(user_id)
        await self.token_service.save_refresh_token(payload)
        print(data)

        return data
