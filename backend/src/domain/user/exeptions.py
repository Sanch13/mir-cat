from src.domain.base_domain_ecxeptions import DomainError


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
