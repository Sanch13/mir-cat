import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.user.interfaces import IPasswordHasher
from src.shared.domain.exceptions import (
    InvalidFormatError,
    PasswordInvalidCharactersError,
    PasswordTooLongError,
    PasswordTooShortError,
)
from src.shared.domain.value_objects import DatetimeVo, StrWithSizeVo, UuidVo

MIN_PASSWORD_LENGTH = 5
MAX_PASSWORD_LENGTH = 70
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
class UserCreatedAtVo(DatetimeVo):
    """
    User creation timestamp Value Object.

    Represents the exact datetime when a user account was created.
    """

    pass


@dataclass(frozen=True)
class UserUpdatedAtVo(DatetimeVo):
    """
    User update timestamp Value Object.

    Represents the last datetime when user information was modified.
    Should be updated on every user profile change.
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

    MAX_SIZE: ClassVar[int] = MAX_NAME_LENGTH


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

    MAX_SIZE: ClassVar[int] = MAX_NAME_LENGTH


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
    """

    MIN_SIZE: ClassVar[int] = MIN_EMAIL_LENGTH
    MAX_SIZE: ClassVar[int] = MAX_EMAIL_LENGTH

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
        if "@" not in self.value:
            raise InvalidFormatError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "expected_format": "email must contain @ symbol",
                    "value": self.value,
                }
            )

        parts = self.value.split("@")
        if len(parts) != 2:
            raise InvalidFormatError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "expected_format": "email must have exactly one @ symbol",
                    "value": self.value,
                }
            )

        local_part, domain = parts

        if not local_part or not domain:
            raise InvalidFormatError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "expected_format": "email must have both local part and domain",
                    "value": self.value,
                }
            )

        if "." not in domain:
            raise InvalidFormatError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "expected_format": "domain must contain a dot",
                    "value": self.value,
                }
            )

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

        if local_part.startswith(".") or local_part.endswith("."):
            raise InvalidFormatError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "expected_format": "local part cannot start or end with dot",
                    "value": self.value,
                }
            )

        if ".." in local_part:
            raise InvalidFormatError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "expected_format": "local part cannot contain consecutive dots",
                    "value": self.value,
                }
            )

    @property
    def domain(self) -> str:
        """
        Extract and return the domain part of the email.

        Returns:
            str: Domain portion after @ symbol
        """
        return self.value.split("@")[1]

    @property
    def local_part(self) -> str:
        """
        Extract and return the local part of the email.

        Returns:
            str: Local portion before @ symbol
        """
        return self.value.split("@")[0]


PASSWORD_RULES_REGEX = {
    "lowercase": re.compile(r"[a-z]"),
    "uppercase": re.compile(r"[A-Z]"),
    "digit": re.compile(r"\d"),
    "special": re.compile(r"[!@#$%^&*(),.?\":{}|<>_\-+=]"),
    "latin_only": re.compile(r"^[A-Za-z0-9!@#$%^&*(),.?\":{}|<>_\-+=]+$"),
}


@dataclass(frozen=True)
class PasswordHashVo:
    value: str

    @classmethod
    def from_hash(cls, hash_str: str) -> "PasswordHashVo":
        """Создать VO из уже хешированного значения (при чтении из БД)."""
        if not hash_str or not isinstance(hash_str, str):
            raise ValueError("hash_str must be non-empty string")
        return cls(value=hash_str)

    @classmethod
    def from_plain(cls, plain: str, hasher: IPasswordHasher) -> "PasswordHashVo":
        """Создать VO из сырого пароля, хешируя его через порт hasher."""
        cls._validate_plain(plain)
        hashed = hasher.hash(plain)
        return cls(value=hashed)

    @property
    def hash(self) -> str:
        return self.value

    def verify(self, plain: str, hasher: IPasswordHasher) -> bool:
        """Проверить сырой пароль против хеша."""
        return hasher.verify(plain, self.value)

    # --- локальные правила валидации пароля (доменная логика) ---
    @staticmethod
    def _validate_plain(plain_password: str):
        if not isinstance(plain_password, str):
            raise ValueError("Password must be a string")

        password = plain_password.strip()
        length = len(password)

        if MIN_PASSWORD_LENGTH is not None and length < MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(
                message_to_extend={
                    "attr_name": "PasswordHashVo",
                    "min_length": MIN_PASSWORD_LENGTH,
                    "current_length": length,
                    "value": "<hidden>",
                }
            )

        if MAX_PASSWORD_LENGTH is not None and length > MAX_PASSWORD_LENGTH:
            raise PasswordTooLongError(
                message_to_extend={
                    "attr_name": "PasswordHashVo",
                    "max_length": MAX_PASSWORD_LENGTH,
                    "current_length": length,
                    "value": "<hidden>",
                }
            )

        if not PASSWORD_RULES_REGEX["latin_only"].match(password):
            raise PasswordInvalidCharactersError(
                message_to_extend={
                    "attr_name": "PasswordHashVo",
                    "value": "<hidden>",
                }
            )
        #  TODO: Обсудить какие критерии пароля такие и выставить правила
        # if not PASSWORD_RULES_REGEX["lowercase"].search(password):
        #     raise ValueError("Пароль должен содержать хотя бы одну строчную букву (a-z)")
        #
        # if not PASSWORD_RULES_REGEX["uppercase"].search(password):
        #     raise ValueError("Пароль должен содержать хотя бы одну заглавную букву (A-Z)")
        #
        # if not PASSWORD_RULES_REGEX["digit"].search(password):
        #     raise ValueError("Пароль должен содержать хотя бы одну цифру")
        #
        # if not PASSWORD_RULES_REGEX["special"].search(password):
        #     raise ValueError("Пароль должен содержать хотя бы один спецсимвол (!@#$%^&* и т. д.)")
