from email.message import EmailMessage

from dishka.integrations.taskiq import FromDishka, inject
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import SMTPSettings, broker
from src.data_access.email.email_sender import EmailSender
from src.data_access.models import UserModel


@broker.task
@inject(patch_module=True)
async def send_email_task(
    to_email: str,
    data: str,
    session: FromDishka[AsyncSession],
    email_sender: FromDishka[EmailSender],
    smtp_settings: FromDishka[SMTPSettings],
) -> None:
    message = EmailMessage()
    message["Subject"] = "тема бла бла"
    message["From"] = smtp_settings.user
    message["To"] = to_email

    query = select(UserModel).where(UserModel.email == data)
    result = await session.execute(query)
    sql_user = result.scalar_one_or_none()
    data = {c.key: getattr(sql_user, c.key) for c in inspect(sql_user).mapper.column_attrs}
    data = "\n".join(f"{k}: {v}" for k, v in data.items())
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
        await email_sender.send_email(message=message)
    except Exception as e:
        print(e)

    print("sent email")
