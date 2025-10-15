from contextvars import ContextVar
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.responses import JSONResponse

from src.apps.base_apps_exception import (
    ApplicationError,
    DatabaseError,
    DatabaseTimedOutError,
    DuplicateEntityError,
    EntityNotFoundError,
    UseCaseError,
)
from src.domain.base_domain_exception import DomainError
from src.shared.domain.exceptions import (
    EmptyValueError,
    FieldNegativeError,
    FieldTooLongError,
    FieldTooShortError,
    FieldZeroError,
    InvalidFormatError,
    InvalidTypeError,
    PasswordInvalidCharactersError,
    PasswordTooLongError,
    PasswordTooShortError,
)

# TODO Логирование и трейсинг
# logger = logging.getLogger(__name__)

# ID для трейсинга
trace_id: ContextVar[str] = ContextVar("trace_id", default="")


class ExceptionHandler:
    def __init__(self):
        self.status_mapping: dict[type[Exception], int] = {
            # Валидационные ошибки
            RequestValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,  # ошибка FastApi
            ValidationException: status.HTTP_400_BAD_REQUEST,
            InvalidFormatError: status.HTTP_400_BAD_REQUEST,
            EmptyValueError: status.HTTP_400_BAD_REQUEST,
            InvalidTypeError: status.HTTP_400_BAD_REQUEST,
            FieldNegativeError: status.HTTP_400_BAD_REQUEST,
            FieldZeroError: status.HTTP_400_BAD_REQUEST,
            FieldTooShortError: status.HTTP_400_BAD_REQUEST,
            FieldTooLongError: status.HTTP_400_BAD_REQUEST,
            PasswordTooShortError: status.HTTP_400_BAD_REQUEST,
            PasswordTooLongError: status.HTTP_400_BAD_REQUEST,
            PasswordInvalidCharactersError: status.HTTP_400_BAD_REQUEST,
            # Ошибки "не найдено"
            EntityNotFoundError: status.HTTP_404_NOT_FOUND,
            # Авторизация/аутентификация
            # InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
            # TokenExpireError: status.HTTP_401_UNAUTHORIZED,
            # TokenRefreshExpireError: status.HTTP_401_UNAUTHORIZED,
            # InviteTokenExpiredError: status.HTTP_401_UNAUTHORIZED,
            # NotActivationExpire: status.HTTP_401_UNAUTHORIZED,
            # TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
            # UserPasswordException: status.HTTP_401_UNAUTHORIZED,
            # Доступ
            # PermissionDeniedException: status.HTTP_403_FORBIDDEN,
            # UserPermissionError: status.HTTP_403_FORBIDDEN,
            # UserNotAdminError: status.HTTP_403_FORBIDDEN,
            # Конфликты
            DuplicateEntityError: status.HTTP_409_CONFLICT,
            # Инфраструктурные
            DatabaseTimedOutError: status.HTTP_503_SERVICE_UNAVAILABLE,
            DatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Подстраховка для необработанных ошибок
            ApplicationError: status.HTTP_400_BAD_REQUEST,  # Основной тип для Apps
            DomainError: status.HTTP_400_BAD_REQUEST,  # Fallback: должен быть пойман в Apps
            UseCaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

        # Маппинг заголовков для ошибок
        self.headers_mapping: dict[type[Exception], dict[str, str]] = {
            DatabaseTimedOutError: {
                "Retry-After": "30",
                "Cache-Control": "no-store, no-cache, must-revalidate",
            },
        }

    async def handle(self, request: Request, exc: Exception) -> JSONResponse:
        exc_type = type(exc)
        status_code = self.status_mapping.get(exc_type, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Получаем заголовки для ошибки, если они есть
        headers = self.headers_mapping.get(exc_type, {})

        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            error_code = "INTERNAL_SERVER_ERROR"
            message = "Internal server error"
            details = None
        else:
            error_code = getattr(exc, "code", exc.__class__.__name__)
            message = getattr(exc, "message", str(exc))
            details = getattr(exc, "details", None)

        # TODO Логирование

        # Формируем базовую структуру ответа
        response_data = {
            "error": {
                "code": str(error_code),
                "message": message,
                "trace_id": trace_id.get(),
            }
        }

        # Добавляем details только если он не None
        if details is not None:
            response_data["error"]["details"] = details

        return JSONResponse(status_code=status_code, content=response_data, headers=headers)


# Глобальный обработчик
exception_handler = ExceptionHandler()


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    trace_id.set(str(uuid4()))
    return await exception_handler.handle(request, exc)


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, global_exception_handler)
