import re
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from src.base_exceptions import ErrorDetails
from src.data_access.base_data_access_exceptions import InfrastructureException
from src.shared.error_codes import ErrorCode

F = TypeVar("F", bound=Callable[..., Any])


def handle_db_errors(func: F) -> F:  # type: ignore  # noqa: UP047
    """
    Декоратор для обработки ошибок базы данных в репозиториях.
    Перехватывает SQLAlchemy-ошибки и преобразует их в InfrastructureException
    с информацией о сущности, операции и деталях ошибки.
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        # Извлекаем имя сущности из класса репозитория (например, "User" из UserRepository)
        entity_name = str(self.__class__.__name__.replace("Repository", ""))
        # Имя операции — имя функции (например, "save", "get_by_id")
        operation = str(func.__name__)

        try:
            return await func(self, *args, **kwargs)

        except IntegrityError as e:
            details: ErrorDetails = {"entity": entity_name, "operation": operation}
            # Проверяем, связана ли ошибка с уникальным ограничением
            if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
                field = "unknown"
                unique_value = "unknown"  # Используем значение из аргументов по умолчанию

                # Парсим DETAIL из сообщения об ошибке
                error_message = str(e)
                match = re.search(r"Key \((.*?)\)=\((.*?)\) already exists", error_message)
                if match:
                    field = match.group(1)  # Например, "email"
                    unique_value = match.group(2)  # Например, "auri@mail.ru"

                details["identifier"] = field
                details["value"] = unique_value
                raise InfrastructureException(
                    message=f"{entity_name} with unique {field} already exists",
                    code=ErrorCode.DUPLICATE_ENTITY,
                    context=e,
                    details=details,
                ) from e
            details["error_type"] = "integrity_violation"
            raise InfrastructureException(
                message=f"Data integrity violation in {entity_name}.{operation}",
                code=ErrorCode.DATA_INTEGRITY_ERROR,
                context=e,
                details=details,
            ) from e

        except OperationalError as e:
            details: ErrorDetails = {
                "entity": entity_name,
                "operation": operation,
                "error_type": "timeout" if "timeout" in str(e).lower() else "operational",
            }
            err = "timeout" if "timeout" in str(e).lower() else "operation failed"
            raise InfrastructureException(
                message=f"Database {err} in {entity_name}.{operation}",
                code=ErrorCode.DATABASE_TIMEOUT
                if "timeout" in str(e).lower()
                else ErrorCode.DATABASE_ERROR,
                context=e,
                details=details,
            ) from e

        except SQLAlchemyError as e:
            details: ErrorDetails = {
                "entity": entity_name,
                "operation": operation,
                "error_type": "sqlalchemy",
            }
            raise InfrastructureException(
                message=f"Unexpected database error in {entity_name}.{operation}",
                code=ErrorCode.DATABASE_ERROR,
                context=e,
                details=details,
            ) from e

    return wrapper
