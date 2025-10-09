from email.message import EmailMessage

import aiosmtplib

from src.config.smtp_settings import SMTPSettings


async def connect_smtp_and_send_email(smtp_config: SMTPSettings, message: EmailMessage) -> None:
    """Подключается к SMTP-серверу и отправляет письмо"""
    try:
        async with aiosmtplib.SMTP(
            hostname=smtp_config.host,
            port=smtp_config.port,
            start_tls=True,  # use_tls=True (порт 465) или start_tls=True (порт 587)
            timeout=10,  # Добавляем таймаут
        ) as server:
            await server.login(smtp_config.user, smtp_config.password)
            await server.send_message(message)
            print("Письмо успешно отправлено")
    except aiosmtplib.SMTPException as e:
        print(f"Ошибка SMTP: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
