from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    """
    Интерфейс находится в домене. Это позволяет VO или доменным сервисам ссылаться на абстракцию,
    а реализация будет в infrastructure (data_access).
    The interface resides in the domain. This allows VOs or domain services to reference
     the abstraction, the implementation being in the infrastructure(data_access).
    """

    @abstractmethod
    def hash(self, plain: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, plain: str, hashed: str) -> bool:
        raise NotImplementedError
