from dishka import AsyncContainer, make_async_container

from src.provides.adapters import (
    AuthenticateUserServiceProvider,
    EmailNotificationServiceProvider,
    EmailProvider,
    JWTServiceProvider,
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
        RedisProvider(),
        PasswordHasherProvider(),
        AuthenticateUserServiceProvider(),
        UserUseCaseProvider(),
        EmailProvider(),
        EmailNotificationServiceProvider(),
        JWTServiceProvider(),
    )
