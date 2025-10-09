# import os
from email.message import EmailMessage

from src.config.smtp_settings import smtp_config
from src.core.bg_tasks.redis_broker import broker
from src.core.bg_tasks.utils import connect_smtp_and_send_email

# Оставлен как пример периодик задачи
# @broker.task(schedule=[{"cron": "*/1 * * * *"}])  # Каждые 1 минут
# async def scheduled_task():
#     await send_email_task.kiq(
#         data="This task runs every 1 minute",
#         email_to=[os.getenv("SMTP_EMAIL_TO")]
#     )
#     return "Scheduled task completed"


@broker.task
async def send_email_task(data: str, email_to: list[str]) -> None:
    message = EmailMessage()
    message["Subject"] = "subject"
    message["From"] = smtp_config.user
    message["To"] = email_to

    message.set_content(data)

    # Оставлен как пример добавления HTML-контент в письмо
    # message.set_content(data, subtype='html')  # Устанавливаем HTML-контент
    # Добавляем plain-text версию для клиентов, не поддерживающих HTML
    # message.add_alternative(data, subtype='plain')
    # Оставлен как пример прикрепления файла в письмо
    # filename = data.get("filename")
    # message.add_attachment(file_stream.read(),
    #                        maintype='application',
    #                        subtype="pdf",
    #                        filename=("utf-8", "", f"{filename}"))

    try:
        await connect_smtp_and_send_email(smtp_config, message)
    except Exception as e:
        print(e)

    print("sent email")
