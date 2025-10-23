from src.domain.base_domain_ecxeptions import DomainError


class EmptyValueError(DomainError):
    """Empty value error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be empty"


class InvalidTypeError(DomainError):
    """Invalid type error."""

    MESSAGE_TEMPLATE = (
        "Expected type '{expected_type}' for field '{attr_name}', but got '{actual_type}'"
    )


class FieldNegativeError(DomainError):
    """Negative error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be negative"


class FieldZeroError(DomainError):
    """Zero error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be zero"


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
        "Current length is {current_length} characters"
    )


class FieldTooLongError(DomainError):
    """Field too long error."""

    MESSAGE_TEMPLATE = (
        "Field '{attr_name}' exceeds maximum length of {max_length} characters. "
        "Got {current_length} characters"
    )


class InvalidFormatError(DomainError):
    """Invalid format error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' has invalid format. Expected format: {expected_format}."
