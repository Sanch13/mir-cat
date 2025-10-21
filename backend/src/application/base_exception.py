from src.base_exceptions import ErrorDetails, TemplateAppError
from src.shared.error_codes import ErrorCode


class ApplicationError(TemplateAppError):
    """Базовое исключение слоя приложения."""

    DEFAULT_CODE = ErrorCode.APPLICATION_ERROR
    DEFAULT_MESSAGE = "Application error occurred"


class EntityNotFoundError(ApplicationError):
    """Сущность не найдена при выполнении Use Case"""

    MESSAGE_TEMPLATE = "{entity} with {criteria} not found"

    @classmethod
    def for_entity(
        cls,
        entity_name: str,
        identifier: str,
        value: str,
        details: ErrorDetails | None = None,
        context: Exception | None = None,
        code: ErrorCode = ErrorCode.ENTITY_NOT_FOUND,
    ) -> "EntityNotFoundError":
        return cls(
            message_to_extend={
                "entity": entity_name.capitalize(),
                "criteria": f"{identifier}={value}",
            },
            code=code,
            context=context,
            details=details,
        )


class DuplicateEntityError(ApplicationError):
    """Сущность с таким уникальным идентификатором уже существует"""

    MESSAGE_TEMPLATE = "{entity} with {criteria} already exists"

    @classmethod
    def for_entity(
        cls,
        entity_name: str,
        identifier: str,
        value: str,
        details: ErrorDetails | None = None,
        context: Exception | None = None,
        code: ErrorCode = ErrorCode.DUPLICATE_ENTITY,
    ) -> "DuplicateEntityError":
        return cls(
            message_to_extend={
                "entity": entity_name.capitalize(),
                "criteria": f"{identifier}={value}",
            },
            code=code,
            context=context,
            details=details,
        )


class DatabaseTimedOutError(ApplicationError):
    """Таймаут подключения к БД"""

    DEFAULT_MESSAGE = "Database connection timed out"
    DEFAULT_CODE = ErrorCode.DATABASE_TIMEOUT


class DatabaseError(ApplicationError):
    """Ошибка в репозитории"""

    DEFAULT_MESSAGE = "Database error"
    DEFAULT_CODE = ErrorCode.DATABASE_ERROR


class UseCaseError(ApplicationError):
    """Базовое исключение для Use Cases"""

    MESSAGE_TEMPLATE = "Use case failed: {use_case_name}"

    @classmethod
    def for_use_case(
        cls,
        use_case_name: str,
        context: Exception | None = None,
        details: ErrorDetails | None = None,
        code: ErrorCode = ErrorCode.USE_CASE_ERROR,
    ) -> "UseCaseError":
        return cls(
            message_to_extend={"use_case_name": use_case_name},
            code=code,
            context=context,
            details=details,
        )


# class ValidationError(ApplicationError):
#     """Ошибка валидации входных данных Use Case"""
#     DEFAULT_CODE = "VALIDATION_ERROR"
#     DEFAULT_MESSAGE = "Validation error"
#     MESSAGE_TEMPLATE = "Validation failed for {entity}"
#
#     @classmethod
#     def for_entity(
#         cls,
#         entity: str,
#         field_errors: Dict[str, str],
#         context: Optional[Exception] = None,
#     ) -> "ValidationError":
#         return cls(
#             message_to_extend={"entity": entity},
#             code=cls.DEFAULT_CODE,
#             context=context,
#             details={"entity": entity, "field_errors": field_errors},
#         )
#
#
# class BusinessRuleViolationError(ApplicationError):
#     """Нарушение бизнес-правил в Use Case"""
#     DEFAULT_CODE = "BUSINESS_RULE_VIOLATION"
#     DEFAULT_MESSAGE = "Business rule violation"
#     MESSAGE_TEMPLATE = "Business rule '{rule_name}' violated"
#
#     @classmethod
#     def for_rule(
#         cls,
#         rule_name: str,
#         context: Optional[Exception] = None,
#         details: Optional[ErrorDetails] = None,
#     ) -> "BusinessRuleViolationError":
#         base_details: ErrorDetails = {"rule": rule_name}
#         if details:
#             base_details.update(details)
#         return cls(
#             message_to_extend={"rule_name": rule_name},
#             code=cls.DEFAULT_CODE,
#             context=context,
#             details=base_details,
#         )
#
#
# class PermissionDeniedError(ApplicationError):
#     """Отказ в доступе при выполнении Use Case"""
#     DEFAULT_CODE = "PERMISSION_DENIED"
#     DEFAULT_MESSAGE = "Permission denied"
#     MESSAGE_TEMPLATE = "Permission denied for action: {action}"
#
#     @classmethod
#     def for_action(
#         cls,
#         action: str,
#         resource: Optional[str] = None,
#         context: Optional[Exception] = None,
#     ) -> "PermissionDeniedError":
#         details: ErrorDetails = {"action": action}
#         if resource:
#             details["resource"] = resource
#         return cls(
#             message_to_extend={"action": action},
#             code=cls.DEFAULT_CODE,
#             context=context,
#             details=details,
#         )
#
# class ConcurrentModificationError(ApplicationError):
#     """Конфликт параллельных изменений в Use Case"""
#     DEFAULT_CODE = "CONCURRENT_MODIFICATION"
#     DEFAULT_MESSAGE = "Concurrent modification detected"
#     MESSAGE_TEMPLATE = "Concurrent modification for {resource}"
#
#     @classmethod
#     def for_resource(
#         cls,
#         resource: str,
#         resource_id: Any,
#         context: Optional[Exception] = None,
#     ) -> "ConcurrentModificationError":
#         return cls(
#             message_to_extend={"resource": resource},
#             code=cls.DEFAULT_CODE,
#             context=context,
#             details={"resource": f'resource: {resource}, resource_id: {resource_id}'}
#         )
#
# class ExternalServiceError(ApplicationError):
#     """Ошибка взаимодействия с внешним сервисом"""
#     DEFAULT_CODE = "EXTERNAL_SERVICE_ERROR"
#     DEFAULT_MESSAGE = "External service error"
#     MESSAGE_TEMPLATE = "External service '{service_name}' error"
#
#     @classmethod
#     def for_service(
#         cls,
#         service_name: str,
#         operation: str,
#         context: Optional[Exception] = None,
#     ) -> "ExternalServiceError":
#         return cls(
#             message_to_extend={"service_name": service_name},
#             code=cls.DEFAULT_CODE,
#             context=context,
#             details={"service": service_name, "operation": operation},
#         )
