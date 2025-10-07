from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user.entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError
