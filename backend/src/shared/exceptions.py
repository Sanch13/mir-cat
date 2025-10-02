from src.base_exceptions import TemplateAppError

class EmptyValueError(TemplateAppError):
    """Empty value error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be empty, but got value: {value}"


class InvalidTypeError(TemplateAppError):
    """Invalid type error."""

    MESSAGE_TEMPLATE = "Expected type '{expected_type}' for field '{attr_name}', but got '{actual_type}' with value: '{value}'"


class FieldNegativeError(TemplateAppError):
    """Negative error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be negative, but got value: {value}"


class FieldZeroError(TemplateAppError):
    """Zero error."""

    MESSAGE_TEMPLATE = "Field '{attr_name}' cannot be zero"


class EntityWithoutIdHashError(TemplateAppError):
    """
    Exception raised when attempting to compute the hash
    of an entity without an assigned ID.
    """

    MESSAGE_TEMPLATE = "Cannot hash an entity of type {entity} without an ID."


class FieldTooShortError(TemplateAppError):
    """Field too short error."""

    MESSAGE_TEMPLATE = (
        "The '{attr_name}' field must be at least {min_length} characters long. "
        "Current length is {current_length} characters: '{value}'"
    )


class FieldTooLongError(TemplateAppError):
    """Field too long error."""

    MESSAGE_TEMPLATE = (
        "Field '{attr_name}' exceeds maximum length of {max_length} characters. "
        "Got {current_length} characters: {value}"
    )

class InvalidFormatError(TemplateAppError):
    """Invalid format error."""

    MESSAGE_TEMPLATE = (
        "Field '{attr_name}' has invalid format. "
        "Expected format: {expected_format}. "
        "Got: {value}"
    )