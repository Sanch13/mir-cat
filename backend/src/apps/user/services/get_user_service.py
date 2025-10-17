from fastapi import HTTPException, Request

from src.apps.user.services.jwt_service import JWTService


class GetCurrentUserService:
    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    async def extract_bearer_token(self, request: Request) -> str:
        """Извлекает и валидирует Bearer токен из запроса"""
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        parts = auth_header.split()

        if len(parts) != 2:
            raise HTTPException(status_code=401, detail="Invalid Authorization header format")

        scheme, token = parts

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        if not token:
            raise HTTPException(status_code=401, detail="Empty token")

        return token

    async def get_current_user_id(self, request: Request) -> str:
        """Получаем user_id из Request"""
        token = await self.extract_bearer_token(request)
        payload = await self.jwt_service.verify_access_token(token)

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return user_id
