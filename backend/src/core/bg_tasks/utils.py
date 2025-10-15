from email.message import EmailMessage

import aiosmtplib

from src.config.settings import Settings


async def connect_smtp_and_send_email(settings: Settings, message: EmailMessage) -> None:
    """Подключается к SMTP-серверу и отправляет письмо"""
    try:
        async with aiosmtplib.SMTP(
            hostname=settings.smtp.host,
            port=settings.smtp.port,
            start_tls=True,  # use_tls=True (порт 465) или start_tls=True (порт 587)
            timeout=10,  # Добавляем таймаут
        ) as server:
            await server.login(settings.smtp.user, settings.smtp.password)
            await server.send_message(message)
            print("Письмо успешно отправлено")
    except aiosmtplib.SMTPException as e:
        print(f"Ошибка SMTP: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
