from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.apps.interfaces import IEmailNotificationService
from src.apps.services import EmailNotificationServiceImpl
from src.apps.user.irepo import IUserRepository
from src.config import DBSettings, SMTPSettings
from src.data_access.email.email_sender import EmailSender
from src.data_access.repositories.user_repo import UserRepository
from src.data_access.services.hasher import PasswordHasherImpl
from src.domain.user.interfaces import IPasswordHasher


class SqlalchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_async_engine(self, db_config: DBSettings) -> AsyncEngine:
        return create_async_engine(db_config.construct_sqlalchemy_url)

    @provide(scope=Scope.APP)
    def provide_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_async_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()
                raise
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def db_settings(self) -> DBSettings:
        return DBSettings()


class EmailProvider(Provider):
    """Провайдер для email инфраструктуры"""

    @provide(scope=Scope.APP)
    def provide_smtp_settings(self) -> SMTPSettings:
        """Настройки SMTP - синглтон"""
        return SMTPSettings()

    @provide(scope=Scope.APP)
    def provide_email_sender(self, settings: SMTPSettings) -> EmailSender:
        """EmailSender - синглтон (stateless)"""
        return EmailSender(settings)

    # TODO: Подумать! Реализовать отдельный сервис по созданию message ?
    # @provide(scope=Scope.APP)
    # def provide_email_message_builder(self, settings: SMTPSettings) -> EmailMessageBuilder:
    #     """EmailMessageBuilder - синглтон (stateless)"""
    #     return EmailMessageBuilder(settings)
    #
    # @provide(scope=Scope.APP)
    # def provide_email_content_builder(self) -> EmailContentBuilder:
    #     """EmailContentBuilder - синглтон (stateless)"""
    #     return EmailContentBuilder()


class EmailNotificationServiceProvider(Provider):
    """Провайдер для Application сервисов в FastAPI"""

    @provide(scope=Scope.APP)
    def provide_email_notification_service(self) -> IEmailNotificationService:
        return EmailNotificationServiceImpl()


class RepositoryProvider(Provider):
    user_repository = provide(source=UserRepository, scope=Scope.REQUEST, provides=IUserRepository)


class PasswordHasherProvider(Provider):
    hasher = provide(source=PasswordHasherImpl, scope=Scope.APP, provides=IPasswordHasher)
