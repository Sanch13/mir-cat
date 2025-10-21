from src.base_exceptions import TemplateAppError


class InfrastructureException(TemplateAppError):
    """Базовое исключение слоя доступа инфраструктуры"""

    DEFAULT_MESSAGE = "Infrastructure error occurred"
