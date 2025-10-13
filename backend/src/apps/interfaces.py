from abc import ABC, abstractmethod


class IEmailNotificationService(ABC):
    @abstractmethod
    def send_email(self, to_email: str, data: str) -> None:
        raise NotImplementedError
