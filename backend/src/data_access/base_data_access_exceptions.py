from src.base_exceptions import TemplateAppError


class InfrastructureException(TemplateAppError):
    """Базовое исключение слоя доступа инфраструктуры"""

    DEFAULT_MESSAGE = "Infrastructure error occurred"


# class RepositoryError(InfrastructureException):
#     """Ошибка в репозитории"""
#     DEFAULT_MESSAGE = "Repository error"
#
# class UniqueConstraintError(RepositoryError):
#     """Нарушение уникальности"""
#     MESSAGE_TEMPLATE = "{field} with this {value} already exists (unique constraint violated)"
#     DEFAULT_CODE = 'SAVE_FAILED'
#
#
# # class DatabaseConnectionError(DataAccessError):
# #     """Ошибка подключения к БД"""
# #     DEFAULT_MESSAGE = "Database connection error"
#
#
# class DatabaseTimedOutError(InfrastructureException):
#     """Ошибка подключения к БД"""
#     DEFAULT_MESSAGE = "Database connection timed out"
#     DEFAULT_CODE = "DATA_BASE_TIME_OUT"
#
#
# class TransactionError(InfrastructureException):
#     """Ошибка транзакции"""
#     MESSAGE_TEMPLATE = "Transaction failed: {transaction_details}"
#     DEFAULT_CODE = "Transaction error"
