from dataclasses import dataclass
from typing import ClassVar

from src.shared.exceptions import InvalidFormatError
from src.shared.value_objects import UuidVo, StrWithSizeVo, DatetimeVo

MIN_PASSWORD_LENGTH = 5
MAX_PASSWORD_LENGTH = 15
MIN_EMAIL_LENGTH = 5
MAX_EMAIL_LENGTH = 254
MAX_NAME_LENGTH = 30


@dataclass(frozen=True)
class UserIdVo(UuidVo):
    """
    User ID Value Object representing a unique user identifier.
    Inherits all UUID validation from UuidVo base class.
    """
    pass


@dataclass(frozen=True)
class UserPasswordVo(StrWithSizeVo):
    """
    User password Value Object with security constraints.

    Enforces minimum and maximum password length for security:
    - Prevents too short passwords (vulnerable to brute force)
    - Prevents excessively long passwords (storage/performance issues)

    Constraints:
        Minimum length: MIN_PASSWORD_LENGTH characters
        Maximum length: MAX_PASSWORD_LENGTH characters

    TO_DO: Установить дополнительные требования к паролю при валидации.
    """
    _MIN_SIZE: ClassVar[int] = MIN_PASSWORD_LENGTH
    _MAX_SIZE: ClassVar[int] = MAX_PASSWORD_LENGTH


@dataclass(frozen=True)
class UserCreatedAtVo(DatetimeVo):
    """
    User creation timestamp Value Object.

    Represents the exact datetime when a user account was created.

    Example:
        >>> from datetime import datetime
        >>> created_at = UserCreatedAtVo(datetime(2023, 12, 31, 14, 30, 0))
    """
    pass


@dataclass(frozen=True)
class UserUpdatedAtVo(DatetimeVo):
    """
    User update timestamp Value Object.

    Represents the last datetime when user information was modified.
    Should be updated on every user profile change.

    Example:
        >>> from datetime import datetime
        >>> updated_at = UserUpdatedAtVo(datetime(2024, 1, 15, 10, 0, 0))
    """
    pass


@dataclass(frozen=True)
class UserFirstNameVo(StrWithSizeVo):
    """
    User first name Value Object with length constraints.

    Ensures first name meets application requirements:
    - Maximum length constraint for database storage
    - No minimum length (allows single-character names if culturally appropriate)

    Constraints:
        Maximum length: MAX_NAME_LENGTH characters
    """
    _MAX_SIZE: ClassVar[int] = MAX_NAME_LENGTH


@dataclass(frozen=True)
class UserLastNameVo(StrWithSizeVo):
    """
    User last name Value Object with length constraints.

    Ensures last name meets application requirements:
    - Maximum length constraint for database storage
    - No minimum length (accommodates various naming conventions)

    Constraints:
        Maximum length: MAX_NAME_LENGTH characters

    """
    _MAX_SIZE: ClassVar[int] = MAX_NAME_LENGTH


@dataclass(frozen=True)
class UserEmailVo(StrWithSizeVo):
    """
    Email address Value Object with comprehensive validation.

    Performs multiple validation layers:
    1. Length constraints (inherited from StrWithSizeVo)
    2. Basic email format validation
    3. Specific email rule validation

    Constraints:
        Minimum length: MIN_EMAIL_LENGTH characters (e.g., a@b.c)
        Maximum length: MAX_EMAIL_LENGTH characters (RFC 5321 limit)

    Validation Rules:
        - Must contain exactly one @ symbol
        - Must have both local part and domain
        - Domain must contain a dot
        - Local part cannot start/end with dot
        - Local part cannot contain consecutive dots

    Example:
        >>> valid_email = UserEmailVo("user@example.com")
        >>> invalid_email = UserEmailVo("invalid.email")  # Raises InvalidFormatError
    """
    _MIN_SIZE: ClassVar[int] = MIN_EMAIL_LENGTH
    _MAX_SIZE: ClassVar[int] = MAX_EMAIL_LENGTH

    def __post_init__(self):
        """
        Extended validation for email-specific rules.

        Execution order:
        1. Parent class validation (length constraints)
        2. Basic email format validation
        3. Specific email rule validation
        """
        super().__post_init__()
        self._validate_email_format()
        self._validate_specific_rules()

    def _validate_email_format(self):
        """
        Validate basic email format structure.

        Checks:
        - Presence of @ symbol
        - Exactly two parts (local and domain)
        - Non-empty local part and domain
        - Domain contains TLD separator (dot)

        Raises:
            InvalidFormatError: If basic email structure is invalid
        """
        if '@' not in self.value:
            raise InvalidFormatError(message_to_extend={
                'attr_name': self.__class__.__name__,
                'expected_format': 'email must contain @ symbol',
                'value': self.value
            })

        parts = self.value.split('@')
        if len(parts) != 2:
            raise InvalidFormatError(message_to_extend={
                'attr_name': self.__class__.__name__,
                'expected_format': 'email must have exactly one @ symbol',
                'value': self.value
            })

        local_part, domain = parts

        if not local_part or not domain:
            raise InvalidFormatError(message_to_extend={
                'attr_name': self.__class__.__name__,
                'expected_format': 'email must have both local part and domain',
                'value': self.value
            })

        if '.' not in domain:
            raise InvalidFormatError(message_to_extend={
                'attr_name': self.__class__.__name__,
                'expected_format': 'domain must contain a dot',
                'value': self.value
            })

    def _validate_specific_rules(self):
        """
        Validate specific email syntax rules.

        Rules based on RFC 5322:
        - Local part cannot start or end with dot
        - Local part cannot contain consecutive dots

        These rules prevent common email formatting errors.
        """
        # Local part validation (before @)
        local_part = self.local_part

        if local_part.startswith('.') or local_part.endswith('.'):
            raise InvalidFormatError(message_to_extend={
                'attr_name': self.__class__.__name__,
                'expected_format': 'local part cannot start or end with dot',
                'value': self.value
            })

        if '..' in local_part:
            raise InvalidFormatError(message_to_extend={
                'attr_name': self.__class__.__name__,
                'expected_format': 'local part cannot contain consecutive dots',
                'value': self.value
            })

    @property
    def domain(self) -> str:
        """
        Extract and return the domain part of the email.

        Returns:
            str: Domain portion after @ symbol

        Example:
            >>> email = UserEmailVo("user@example.com")
            >>> email.domain
            'example.com'
        """
        return self.value.split('@')[1]

    @property
    def local_part(self) -> str:
        """
        Extract and return the local part of the email.

        Returns:
            str: Local portion before @ symbol

        Example:
            >>> email = UserEmailVo("user.name@example.com")
            >>> email.local_part
            'user.name'
        """
        return self.value.split('@')[0]