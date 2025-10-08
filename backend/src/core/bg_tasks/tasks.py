from email.message import EmailMessage

from src.config.smtp_settings import smtp_config
from src.core.bg_tasks.redis_broker import broker
from src.core.bg_tasks.utils import connect_smtp_and_send_email


@broker.task
async def example_task(name: str) -> str:
    print(f"Hello, {name}!")
    return f"Hello, {name}!"


@broker.task(schedule=[{"cron": "*/1 * * * *"}])  # Каждые 1 минут
async def scheduled_task():
    print("🕒 Scheduled task started!")  # Check if this appears in the worker logs
    await send_email_task.kiq("This task runs every 1 minute")
    print("✅ Scheduled task completed")
    return "Scheduled task completed"


@broker.task
async def send_email_task(data: str) -> None:
    message = EmailMessage()
    message["Subject"] = "subject"
    message["From"] = smtp_config.user
    message["To"] = "a.zubchyk@miran-bel.com"

    message.set_content(data)

    # message.set_content(data, subtype='html')  # Устанавливаем HTML-контент
    # Добавляем plain-text версию для клиентов, не поддерживающих HTML
    # message.add_alternative(data, subtype='plain')

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
