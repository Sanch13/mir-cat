from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from src.application.base_exception import (
    ApplicationError,
    DatabaseError,
    DatabaseTimedOutError,
    DuplicateEntityError,
    ExternalServiceError,
)
from src.domain.base_domain_ecxeptions import DomainError
from src.infrastructure.base_exceptions import (
    DatabaseException,
    DatabaseTimedOutException,
    InfrastructureException,
    UniqueViolationError,
)

F = TypeVar("F", bound=Callable[..., Any])


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
        except UniqueViolationError as e:
            raise DuplicateEntityError.for_entity(
                entity_name=e.details.get("entity", "Entity"),
                identifier=e.details.get("identifier", ""),
                context=e,
                details=e.details.get("details"),
            )

        except DatabaseTimedOutException as e:
            raise DatabaseTimedOutError(context=e, details=e.details or {})

        except DatabaseException as e:
            raise DatabaseError(context=e, details=e.details or {})

        except InfrastructureException as e:
            raise ExternalServiceError(context=e, details=e.details or {})

        except (SystemExit, KeyboardInterrupt):
            # Критические системные исключения пробрасываем
            raise

        # Неожиданные ошибки преобразуем в ApplicationError
        except Exception as e:
            raise ApplicationError(message="Unexpected infrastructure error occurred", context=e)

    return wrapper
