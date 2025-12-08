from uuid import UUID

import structlog
from fastapi import HTTPException, Request

from src.application.interfaces import IAuthTokenService
from src.core.tracing import traced


class GetCurrentUserService:
    """
    Service for extracting and validating current user from HTTP request.

    Provides functionality for:
    - Extracting Bearer token from Authorization headers
    - Validating token format
    - Verifying JWT tokens
    - Extracting user identifier from token payload

    This service acts as an abstraction layer between HTTP request handling
    and JWT token verification, following single responsibility principle.

    Attributes:
        jwt_service (JWTService): Service for JWT token operations
    """

    def __init__(self, token_service: IAuthTokenService):
        self.token_service = token_service

    async def extract_bearer_token(self, request: Request) -> str:
        """
        Extracts and validates Bearer token from Authorization header.

        Performs comprehensive validation:
        - Checks presence of Authorization header
        - Validates 'Bearer <token>' format
        - Ensures 'Bearer' scheme is used
        - Verifies token is not empty

        Args:
            request: FastAPI Request object containing HTTP headers

        Returns:
            str: Valid JWT token string

        Raises:
            HTTPException: 401 status code with detailed error message
                if header is missing or invalid
        """
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

    async def get_payload_from_access_token(self, request: Request) -> dict:
        token = await self.extract_bearer_token(request)
        return await self.token_service.verify_access_token(token)

    @traced(name="auth.get_current_user")
    async def get_current_user_id(self, request: Request) -> UUID:
        """Получаем user_id из payload"""
        payload = await self.get_payload_from_access_token(request)
        await self.is_access_token_in_blacklist(payload)

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid payload. User not found")

        structlog.contextvars.bind_contextvars(user_id=str(user_id))
        return UUID(user_id)

    @traced(name="auth.check_blacklist")
    async def is_access_token_in_blacklist(self, payload: dict) -> bool:
        access_jti = payload.get("jti")
        return await self.token_service.exists_access_token_in_blacklist(access_jti)
