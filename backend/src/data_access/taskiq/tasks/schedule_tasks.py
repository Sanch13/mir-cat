# from email.message import EmailMessage
#
# from dishka.integrations.taskiq import FromDishka, inject
#
# from src.config import broker
# from src.data_access.email import EmailSender


# Оставлен как пример периодик задачи
# @broker.task(schedule=[{"cron": "*/1 * * * *"}])  # Каждые 1 минут
# @inject(patch_module=True)
# async def scheduled_task(email_sender: FromDishka[EmailSender]) -> None:
#     message = EmailMessage()
#     message["Subject"] = "Scheduled task"
#     message["From"] = email_sender.settings.user
#     message['To'] = "a.zubchyk@miran-bel.com"  # указать адоес куда нужно отправлять
#     message.set_content("Scheduled task completed")
#
#     try:
#         await email_sender.send_email(message=message)
#     except Exception as e:
#         print(e)
#
#     print("sent email")
