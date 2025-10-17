from email.message import EmailMessage

from dishka.integrations.taskiq import FromDishka, inject

from src.config import broker
from src.data_access.email import EmailSender


@broker.task
@inject(patch_module=True)
async def send_email_task(
    to_email: str,
    data: str,
    email_sender: FromDishka[EmailSender],
) -> None:
    message = EmailMessage()
    message["Subject"] = "Регистрация пользователя"
    message["From"] = email_sender.settings.user
    message["To"] = to_email
    message.set_content(f"Зарегистрировался пользователь с email: {data}")

    try:
        await email_sender.send_email(message=message)
    except Exception as e:
        print(e)
    print("sent email")
