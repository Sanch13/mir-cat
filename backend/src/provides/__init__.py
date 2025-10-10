from dishka import AsyncContainer, make_async_container

from src.provides.adapters import (
    ConfigProvider,
    PasswordHasherProvider,
    RepositoryProvider,
    SMTPConfigProvider,
    SqlalchemyProvider,
)
from src.provides.usecases import UserUseCaseProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        SqlalchemyProvider(),
        ConfigProvider(),
        RepositoryProvider(),
        PasswordHasherProvider(),
        SMTPConfigProvider(),
        UserUseCaseProvider(),
    )
