from collections.abc import AsyncIterable

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
from taskiq_redis import RedisStreamBroker

from src.apps.user.irepo import IUserRepository
from src.config.db_settings import DBSettings, db_settings
from src.config.redis_settings import RedisSettings
from src.data_access.repositories.user_repo import UserRepository


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
    def provide_db_settings(self) -> DBSettings:
        return db_settings


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    user_repository = provide(UserRepository, provides=IUserRepository)


class RedisSettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_redis_settings(self) -> RedisSettings:
        return RedisSettings()


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_async_redis_pool(self, settings: RedisSettings) -> ConnectionPool:
        """Асинхронный пул подключений для Taskiq"""
        return ConnectionPool.from_url(
            settings.redis_url, decode_responses=True, max_connections=10
        )

    @provide(scope=Scope.APP)
    def provide_async_redis_client(self, pool: ConnectionPool) -> AsyncRedis:
        """Создает асинхронный клиент Redis"""
        # Redis-клиент из пула подключений
        return AsyncRedis(connection_pool=pool)

    @provide(scope=Scope.APP)
    def provide_taskiq_broker(self, settings: RedisSettings) -> RedisStreamBroker:
        """Taskiq брокер для Redis"""
        broker = RedisStreamBroker(
            url=settings.redis_url,
            # Дополнительные настройки при необходимости
        )

        @broker.on_startup
        async def startup() -> None:
            await broker.startup()

        @broker.on_shutdown
        async def shutdown() -> None:
            await broker.shutdown()

        return broker
