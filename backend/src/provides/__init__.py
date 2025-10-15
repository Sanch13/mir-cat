from dishka import AsyncContainer, make_async_container

from src.provides.adapters import (
    AuthenticateUserServiceProvider,
    PasswordHasherProvider,
    RedisProvider,
    RepositoryProvider,
    SettingsProvider,
    SqlalchemyProvider,
)
from src.provides.usecases import UserUseCaseProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        SqlalchemyProvider(),
        SettingsProvider(),
        RepositoryProvider(),
        PasswordHasherProvider(),
        UserUseCaseProvider(),
        AuthenticateUserServiceProvider(),
        RedisProvider(),
    )
