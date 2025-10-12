from abc import ABC, abstractmethod


class IEmailNotificationService(ABC):
    @abstractmethod
    def send_email(
        self,
        to_email: str,
        data: str,
        # subject: str,
        # html_content: str,
        # plain_content: str | None = None
    ) -> None:
        raise NotImplementedError
