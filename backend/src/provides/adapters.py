from collections.abc import AsyncGenerator, AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as AsyncRedis
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
from src.apps.user.services.auth_user_service import AuthenticateUserService
from src.apps.user.services.jwt_service import JWTService
from src.config import all_settings
from src.config.settings import Settings
from src.data_access.email.email_sender import EmailSender
from src.data_access.repositories.user_repo import UserRepository
from src.data_access.services.hasher import PasswordHasherImpl
from src.domain.user.interfaces import IPasswordHasher


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_all_settings(self) -> Settings:
        return all_settings


class SqlalchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_async_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(settings.db.construct_sqlalchemy_url)

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


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis_pool(self, settings: Settings) -> ConnectionPool:
        return ConnectionPool.from_url(settings.redis.redis_url, decode_responses=True)

    @provide(scope=Scope.REQUEST, provides=AsyncRedis)
    async def get_redis_client(self, pool: ConnectionPool) -> AsyncGenerator[AsyncRedis]:
        client = AsyncRedis(connection_pool=pool)
        try:
            yield client
        finally:
            await client.aclose()


class EmailProvider(Provider):
    """Провайдер для email инфраструктуры"""

    @provide(scope=Scope.APP)
    def provide_email_sender(self, settings: Settings) -> EmailSender:
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


class AuthenticateUserServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_auth_user_service(
        self, user_repo: IUserRepository, hasher: IPasswordHasher
    ) -> AuthenticateUserService:
        return AuthenticateUserService(user_repo, hasher)


class JWTServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_jwt_service(self, settings: Settings, redis_client: AsyncRedis) -> JWTService:
        return JWTService(settings, redis_client)
