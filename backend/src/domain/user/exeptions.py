from src.domain.base_domain_ecxeptions import DomainError


class EmailInvalidFormatError(DomainError):
    """Email invalid format error."""

    MESSAGE_TEMPLATE = "The email has invalid format: {violated_rule}."


class EmailInvalidCharactersError(DomainError):
    """The email contains invalid characters"""

    MESSAGE_TEMPLATE = "The email contains invalid characters! {errors}"


class PasswordTooShortError(DomainError):
    """The password is too short"""

    MESSAGE_TEMPLATE = (
        "The password is too short!"
        "The '{attr_name}' field must be at least {min_length} characters long."
        "Current length is {current_length} characters"
    )


class PasswordTooLongError(DomainError):
    """The password is too long"""

    MESSAGE_TEMPLATE = (
        "The password is too long!"
        "The '{attr_name}' field must be at least {min_length} characters long."
        "Current length is {current_length} characters"
    )


class PasswordInvalidCharactersError(DomainError):
    """The password contains invalid characters"""

    MESSAGE_TEMPLATE = (
        "The password contains invalid characters! "
        "The '{attr_name}' field must include only latin letters, digits and special symbols. "
    )


class PasswordInvalidLowercaseError(DomainError):
    """The password must contain at least one lowercase letter (a-z)"""

    MESSAGE_TEMPLATE = "The password must contain at least one lowercase letter (a-z)"


class PasswordInvalidUppercaseError(DomainError):
    """The password must contain at least one uppercase letter (A-Z)"""

    MESSAGE_TEMPLATE = "The password must contain at least one uppercase letter (A-Z)"


class PasswordInvalidDigitError(DomainError):
    """The password must contain at least one number (0-9)"""

    MESSAGE_TEMPLATE = "The password must contain at least one number (0-9)"
