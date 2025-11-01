from abc import ABC, abstractmethod


class IEmailNotificationService(ABC):
    @abstractmethod
    async def send_email(self, to_email: str, data: str) -> None:
        raise NotImplementedError


class IRefreshTokenRepository(ABC):
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
