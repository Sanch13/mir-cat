from abc import ABC, abstractmethod


class IEmailNotificationService(ABC):
    @abstractmethod
    async def send_email(self, to_email: str, data: str) -> None:
        raise NotImplementedError


class ITokenRepository(ABC):
    """Интерфейс для работы с refresh token storage"""

    @abstractmethod
    async def save(self, payload: dict, ttl_seconds: int) -> None:
        """Сохраняет refresh token"""
        pass

    @abstractmethod
    async def exists(self, user_id: str, jti: str) -> bool:
        """Проверяет существование токена"""
        pass

    @abstractmethod
    async def delete(self, user_id: str, jti: str) -> None:
        """Удаляет токен"""
        pass

    @abstractmethod
    async def delete_all_for_user(self, user_id: str) -> None:
        """Удаляет все токены пользователя"""
        pass

    @abstractmethod
    async def count_for_user(self, user_id: str) -> int:
        """Считает токены пользователя"""
        pass

    @abstractmethod
    async def save_access_token_in_blacklist(self, access_jti: str, ttl_seconds: int) -> None:
        """
        Добавляет access_token в blacklist для немедленной инвалидации.

        Используется при logout для отзыва текущего access_token.
        """
        pass

    @abstractmethod
    async def exists_access_token_in_blacklist(self, access_jti: str) -> bool:
        """Проверяет, находится ли access_token в blacklist"""
        pass


class IAuthTokenService(ABC):
    @abstractmethod
    async def create_token_pair(self, user_id: str) -> tuple:
        """Создает пару токенов"""
        raise NotImplementedError

    @abstractmethod
    async def save_refresh_token(self, payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def verify_access_token(self, token: str | None) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def verify_refresh_token(self, refresh_token: str | None) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def exists_refresh_token(self, user_id: str, jti: str):
        raise NotImplementedError

    @abstractmethod
    async def delete_refresh_token(self, user_id: str, jti: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save_access_token_in_blacklist(self, access_jti: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists_access_token_in_blacklist(self, access_jti: str):
        raise NotImplementedError
