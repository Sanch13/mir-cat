from src.base_exceptions import TemplateAppError


class DomainError(TemplateAppError):
    """Базовое исключение слоя domain"""

    DEFAULT_MESSAGE = "Domain error occurred"
    MESSAGE_TEMPLATE = None
