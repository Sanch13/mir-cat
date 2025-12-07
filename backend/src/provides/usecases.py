from dishka import Provider, Scope, provide

from src.application.auth.use_case.auth_use_case import AuthUserUseCase
from src.application.auth.use_case.logout_use_case import LogoutUseCase
from src.application.auth.use_case.refresh_token_use_case import RefreshTokenUseCase
from src.application.user.use_cases.create_use_case import UserCreateUseCase
from src.application.user.use_cases.get_by_id_use_case import UserGetByIdUseCase


class UserUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_user_usecase = provide(UserCreateUseCase)
    get_user_usecase = provide(UserGetByIdUseCase)
    auth_usecase = provide(AuthUserUseCase)
    refresh_token_usecase = provide(RefreshTokenUseCase)
    logout_token_usecase = provide(LogoutUseCase)
