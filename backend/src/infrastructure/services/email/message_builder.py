from email.message import EmailMessage

from src.config.settings import Settings


class EmailMessageBuilder:
    """Низкоуровневый сервис создания message для email"""

    def __init__(self, settings: Settings):
        self.settings = settings.smtp

    async def get_message(self) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = ""
        message["From"] = self.settings.user
        message["To"] = self.settings.user
        return message
