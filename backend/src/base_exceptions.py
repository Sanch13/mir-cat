from typing import Any

from typing_extensions import TypedDict

from src.shared.error_codes import ErrorCode


class ErrorDetails(TypedDict, total=False):
    """Типизация для details, чтобы стандартизировать ключи
    Поля и случаи использования:
    - entity: Название сущности, к которой относится ошибка (напр., "User", "Project").
      Используется в EntityNotFoundError, ValidationError, BusinessRuleViolationError.
    - identifier: Идентификатор сущности (напр., UUID, email, строка). Используется для указания,
      какая сущность не найдена или вызвала ошибку (напр., user_id, email).
    - field_errors: Словарь с ошибками валидации полей (напр., {"email": "Invalid format"}).
      Используется в ValidationError для передачи ошибок валидации.
    - rule: Название нарушенного бизнес-правила (напр., "unique_email", "user_must_be_active").
      Используется в BusinessRuleViolationError.
    - action: Действие, вызвавшее ошибку (напр., "update", "delete").
    Используется в PermissionDeniedError.
    - resource: Ресурс, связанный с ошибкой (напр., "profile", "settings"). Используется в
      PermissionDeniedError, ConcurrentModificationError.
    - service: Название внешнего сервиса (напр., "EmailService", "FileStorage").
    Используется в ExternalServiceError.
    - operation: Операция сервиса, вызвавшая ошибку (напр., "send_email", "upload_file").
      Используется в ExternalServiceError.
    """

    entity: str
    identifier: Any
    value: str
    field_errors: dict[str, str]
    rule: str
    action: str
    resource: str
    service: str
    operation: str
    template_error: str
    error_type: str


class AppError(Exception):
    """
    Base application-level exception to provide consistent error handling.
    Attributes:
        code: Unique error code for API responses and logging.
        message: Human-readable error message.
        details: Additional structured data for error context.
        context: Original exception that caused this error (for chaining).
    """

    DEFAULT_CODE = ErrorCode.BASE_APPLICATION_ERROR
    DEFAULT_MESSAGE = "Base application error occurred"

    def __init__(
        self,
        message: str | None = None,
        code: ErrorCode | None = None,
        context: Exception | None = None,
        details: ErrorDetails | None = None,
    ) -> None:
        self.code = code or self.DEFAULT_CODE
        self.message = message or self.DEFAULT_MESSAGE
        self.details = details
        self.context = context
        super().__init__(self.message)
        if context:
            self.__cause__ = context

    def __str__(self) -> str:
        context_str = (
            f" (caused by {self.context.__class__.__name__}: {self.context})"
            if self.context
            else ""
        )
        return f"[{self.code}] {self.message}{context_str}"


class TemplateAppError(AppError):
    """
    TemplateAppError extends AppError with dynamic message templating.
    Attributes:
        MESSAGE_TEMPLATE: String template for formatting error messages.
        message_to_extend: Dict with values to fill the template.
    """

    MESSAGE_TEMPLATE: str | None = None

    def __init__(
        self,
        message: str | None = None,
        code: ErrorCode | None = None,
        context: Exception | None = None,
        message_to_extend: dict[str, Any] | None = None,
        details: ErrorDetails | None = None,
    ) -> None:
        if message is None and self.MESSAGE_TEMPLATE is not None:
            try:
                message = (
                    self.MESSAGE_TEMPLATE.format_map(message_to_extend)
                    if message_to_extend
                    else self.MESSAGE_TEMPLATE
                )
            except KeyError as e:
                message = self.DEFAULT_MESSAGE
                details = details or {}
                details["template_error"] = f"Missing keys for template: {e}"
        super().__init__(message=message, code=code, context=context, details=details)
