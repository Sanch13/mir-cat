from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from src.apps.base_apps_exception import (
    ApplicationError,
    DatabaseError,
    DatabaseTimedOutError,
    DuplicateEntityError,
    UseCaseError,
)
from src.base_exceptions import ErrorDetails
from src.data_access.base_data_access_exceptions import InfrastructureException
from src.domain.base_domain_exception import DomainError
from src.shared.error_codes import ErrorCode

F = TypeVar("F", bound=Callable[..., Any])

err_mapper = {
    ErrorCode.DUPLICATE_ENTITY: DuplicateEntityError.for_entity,
    ErrorCode.DATA_INTEGRITY_ERROR: DatabaseError,
    ErrorCode.DATABASE_TIMEOUT: DatabaseTimedOutError,
    ErrorCode.DATABASE_ERROR: DatabaseError,
}


def handle_db_errors(func: F) -> F:  # type: ignore  # noqa: UP047
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)

        # Пробрасываем все исключения, наследующиеся от ApplicationError
        except ApplicationError:
            raise

        # Пока пробрасываем все исключения, наследующиеся от DomainError
        # (возможно, стоит трансформировать)
        except DomainError:
            raise

        # Ошибки инфраструктуры трансформируем в ошибки ApplicationError
        except InfrastructureException as e:
            details_from_db = e.details or {}
            entity = details_from_db.get("entity")
            operation = details_from_db.get("operation")
            identifier = details_from_db.get("identifier")
            value = details_from_db.get("value")

            details_apps: ErrorDetails = {"entity": str(entity), "operation": str(operation)}

            app_err = err_mapper.get(e.code)

            if e.code == ErrorCode.DUPLICATE_ENTITY:
                details_apps["identifier"] = identifier
                details_apps["value"] = str(value)

                raise DuplicateEntityError.for_entity(
                    entity_name=entity,
                    identifier=identifier,
                    value=details_from_db.get("value"),
                    context=e,
                    details=details_apps,
                )

            else:
                raise app_err(context=e, details=details_apps)

        except (SystemExit, KeyboardInterrupt):
            # Критические системные исключения пробрасываем
            raise

        # Неожиданные ошибки логируем и преобразуем в UseCaseError
        except Exception as e:
            raise UseCaseError.for_use_case(
                use_case_name=self.__class__.__name__,
                context=e,
                details={
                    "entity": "Unknown",
                    "operation": func.__name__,
                    "error_type": "unexpected",
                },
            )

    return wrapper
