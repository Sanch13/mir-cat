from src.base_exceptions import TemplateAppError


class InfrastructureException(TemplateAppError):
    """Базовое исключение слоя доступа инфраструктуры"""

    DEFAULT_MESSAGE = "Infrastructure error occurred"


class DatabaseException(InfrastructureException):
    """Базовое исключение базы данных"""

    DEFAULT_MESSAGE = "Database error occurred"


class UniqueViolationError(DatabaseException):
    MESSAGE_TEMPLATE = "{entity_name} with unique {field} already exists"


class DatabaseTimedOutException(DatabaseException):
    DEFAULT_MESSAGE = "Database connection timed out"
