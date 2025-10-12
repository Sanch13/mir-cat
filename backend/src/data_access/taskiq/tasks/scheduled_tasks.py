from src.config import broker
from src.data_access.taskiq.tasks.email_tasks import send_email_task


# Оставлен как пример периодик задачи
@broker.task(schedule=[{"cron": "*/1 * * * *"}])  # Каждые 1 минут
async def scheduled_task():
    await send_email_task.kiq(
        user_id="8fd4c0c8-e3a4-4001-af0f-2d6763436bf0",
    )
    return "Scheduled task completed"
