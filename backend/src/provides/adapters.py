from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.apps.user.irepo import IUserRepository
from src.config.db_settings import DBSettings, db_settings
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
