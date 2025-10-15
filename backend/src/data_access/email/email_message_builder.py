from email.message import EmailMessage

from src.config import SMTPSettings


class EmailMessageBuilder:
    """Низкоуровневый сервис создания message для email"""

    def __init__(self, settings: SMTPSettings):
        self.settings = settings

    async def get_message(self) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = ""
        message["From"] = self.settings.user
        message["To"] = self.settings.user
        return message
