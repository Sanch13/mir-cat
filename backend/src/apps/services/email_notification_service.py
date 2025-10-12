from src.apps.interfaces import IEmailNotificationService
from src.data_access.taskiq.tasks.email_tasks import send_email_task


class EmailNotificationService(IEmailNotificationService):
    """
    Application Service для управления email уведомлениями
    Координирует отправку через TaskIQ
    """

    # async def send_welcome_email(self, user_id: int) -> None:
    #     """Отправляет приветственное письмо (async через TaskIQ)"""
    #     await send_welcome_email_task.kiq(user_id=user_id)
    #
    # async def send_password_reset(self, email: str, token: str) -> None:
    #     """Отправляет письмо сброса пароля"""
    #     await send_password_reset_task.kiq(email=email, reset_token=token)

    async def send_email(
        self,
        to_email: str,
        data: str,
        # subject: str,
        # html_content: str,
        # plain_content: str | None = None
    ) -> None:
        """Отправляет произвольное email"""
        await send_email_task.kiq(
            to_email=to_email,
            data=data,
            # subject=subject,
            # html_content=html_content,
            # plain_content=plain_content
        )
