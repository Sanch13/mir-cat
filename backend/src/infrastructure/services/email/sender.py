from email.message import EmailMessage

import aiosmtplib

from src.config.settings import Settings


class EmailSender:
    """Низкоуровневый сервис отправки email"""

    def __init__(self, settings: Settings):
        self.settings = settings.smtp

    async def send_email(self, message: EmailMessage) -> None:
        """Подключается к SMTP-серверу и отправляет письмо"""

        try:
            async with aiosmtplib.SMTP(
                hostname=self.settings.host,
                port=self.settings.port,
                start_tls=True,  # use_tls=True (порт 465) или start_tls=True (порт 587)
                timeout=10,  # Добавляем таймаут
            ) as server:
                await server.login(self.settings.user, self.settings.password)
                await server.send_message(message)
                print("Письмо успешно отправлено")
        except aiosmtplib.SMTPException as e:
            print(f"Ошибка SMTP: {e}")
        except Exception as e:
            print(f"Общая ошибка: {e}")
