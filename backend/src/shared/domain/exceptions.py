from src.base_exceptions import TemplateAppError
from src.domain.base_domain_exception import DomainError
from src.shared.error_codes import ErrorCode


class EmptyValueError(DomainError):
    """Empty value error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be empty, but got value: {value}"
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class InvalidTypeError(DomainError):
    """Invalid type error."""

    MESSAGE_TEMPLATE = (
        "Expected type '{expected_type}' for field '{attr_name}', "
        "but got '{actual_type}' with value: '{value}'"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class FieldNegativeError(DomainError):
    """Negative error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be negative, but got value: {value}"
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class FieldZeroError(DomainError):
    """Zero error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be zero"
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class EntityWithoutIdHashError(DomainError):
    """
    Exception raised when attempting to compute the hash
    of an entity without an assigned ID.
    """

    MESSAGE_TEMPLATE = "Cannot hash an entity of type {entity} without an ID."


class FieldTooShortError(DomainError):
    """Field too short error."""

    MESSAGE_TEMPLATE = (
        "The '{attr_name}' field must be at least {min_length} characters long. "
        "Current length is {current_length} characters: '{value}'"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class FieldTooLongError(DomainError):
    """Field too long error."""

    MESSAGE_TEMPLATE = (
        "Field '{attr_name}' exceeds maximum length of {max_length} characters. "
        "Got {current_length} characters: {value}"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class InvalidFormatError(DomainError):
    """Invalid format error."""

    MESSAGE_TEMPLATE = (
        "Field '{attr_name}' has invalid format. Expected format: {expected_format}. Got: {value}"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class PasswordTooShortError(DomainError):
    """The password is too short"""

    MESSAGE_TEMPLATE = (
        "The password is too short!"
        "The '{attr_name}' field must be at least {min_length} characters long."
        "Current length is {current_length} characters: '{value}'"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class PasswordTooLongError(TemplateAppError):
    """The password is too long"""

    MESSAGE_TEMPLATE = (
        "The password is too long!"
        "The '{attr_name}' field must be at least {min_length} characters long."
        "Current length is {current_length} characters: '{value}'"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR


class PasswordInvalidCharactersError(TemplateAppError):
    """The password contains invalid characters"""

    MESSAGE_TEMPLATE = (
        "The password contains invalid characters! "
        "The '{attr_name}' field must include only latin letters, digits and special symbols. "
        "Provided value: '{value}'"
    )
    DEFAULT_CODE = ErrorCode.VALIDATION_ERROR
