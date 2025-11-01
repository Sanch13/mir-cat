import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.user.exeptions import (
    EmailInvalidCharactersError,
    EmailInvalidFormatError,
    PasswordInvalidCharactersError,
    PasswordInvalidDigitError,
    PasswordInvalidLowercaseError,
    PasswordInvalidUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)
from src.domain.user.interfaces import IPasswordHasher
from src.shared.exceptions import InvalidTypeError
from src.shared.value_objects import DatetimeVo, StrWithSizeVo, UuidVo

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
        3. Validation of allowed chars
        4. Specific email rule validation
        """
        super().__post_init__()
        self._validate_email_format()
        self._validate_email_symbols()
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
            EmailInvalidFormatError: If basic email structure is invalid
        """
        if "@" not in self.value:
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "email must contain @ symbol",
                }
            )

        parts = self.value.split("@")
        if len(parts) != 2:
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "email must have exactly one @ symbol",
                }
            )

        local_part, domain = parts

        if not local_part or not domain:
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "email must have both local part and domain",
                }
            )

        parts = domain.split(".")

        if len(parts) < 2:
            raise EmailInvalidFormatError(
                message_to_extend={"violated_rule": "domain must contain at least one dot"}
            )

        top_level_domain = parts[-1]

        if not top_level_domain:
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "domain must contain top level domain after a dot",
                }
            )

    def _validate_email_symbols(self):
        """
        Validate email characters against allowed character sets.

        This method checks both local part (before @) and domain part (after @)
        for invalid characters based on RFC 5322 specifications.

        Local part allowed characters:
        - Letters: a-z, A-Z
        - Digits: 0-9
        - Special: . ! # $ % & ' * + / = ? ^ _ ` { | } ~ -

        Domain part allowed characters:
        - Letters: a-z, A-Z
        - Digits: 0-9
        - Hyphen: -
        - Dot: . (as separator)

        Raises:
            EmailInvalidCharactersError: If invalid characters are found
                                       in either local or domain part.
        """
        errors = []
        local_allowed_pattern = r"^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+$"
        domain_allowed_pattern = r"^[a-zA-Z0-9.-]+$"

        invalid_local_part_chars = self._get_invalid_chars(self.local_part, local_allowed_pattern)
        if invalid_local_part_chars:
            errors.append(
                f"Local part (before @) contains invalid characters: {invalid_local_part_chars}."
            )

        special_chars_pattern = r"^[^!#$%&\'*+/=?^_`{|}~-]+$"
        invalid_first_and_last = self._get_invalid_chars(
            self.local_part[0] + self.local_part[-1], special_chars_pattern
        )
        if invalid_first_and_last:
            errors.append(
                f"First/last symbol of local part (before @) contains invalid characters: "
                f"{invalid_first_and_last}."
            )

        invalid_domain_chars = self._get_invalid_chars(self.domain, domain_allowed_pattern)
        if invalid_domain_chars:
            errors.append(
                f"Domain part (after @) contains invalid characters: {invalid_domain_chars}."
            )

        if errors:
            raise EmailInvalidCharactersError(
                message_to_extend={
                    "errors": f"{' '.join(errors)}",
                }
            )

    @staticmethod
    def _get_invalid_chars(string: str, pattern: str):
        """
        Find and return invalid characters in a string based on regex pattern.

        Args:
            string: The string to validate
            pattern: Regex pattern that matches allowed individual characters

        Returns:
            str: Comma-separated string of invalid characters in format 'char',
                 or None if all characters are valid
        """
        invalid_chars = set()
        for char in string:
            if not re.match(pattern, char):
                invalid_chars.add(char)

        if invalid_chars:
            return ", ".join([f"'{char}'" for char in invalid_chars])

    def _validate_specific_rules(self):
        """
        Validate specific email syntax rules.

        Rules based on RFC 5322:
        - Local part cannot start or end with dot
        - Local part cannot contain consecutive dots
        - Domain cannot start or end with dot hyphen

        These rules prevent common email formatting errors.

        Raises:
            EmailInvalidFormatError: If specific email rules are violated.
        """
        if ".." in self.value:
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "email cannot contain consecutive dots",
                }
            )

        # Local part validation (before @)
        local_part = self.local_part

        if local_part.startswith(".") or local_part.endswith("."):
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "local part cannot start or end with dot",
                }
            )

        # Domain validation (after @)
        domain = self.domain

        if domain.startswith("-") or domain.endswith("-"):
            raise EmailInvalidFormatError(
                message_to_extend={
                    "violated_rule": "domain cannot start or end with hyphen",
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


MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 70
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
            raise InvalidTypeError(
                message_to_extend={
                    "expected_type": "string",
                    "attr_name": "password",
                    "actual_type": type(plain_password).__name__,
                }
            )

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
        if not PASSWORD_RULES_REGEX["lowercase"].search(password):
            raise PasswordInvalidLowercaseError()

        if not PASSWORD_RULES_REGEX["uppercase"].search(password):
            raise PasswordInvalidUppercaseError()

        if not PASSWORD_RULES_REGEX["digit"].search(password):
            raise PasswordInvalidDigitError()

        # if not PASSWORD_RULES_REGEX["special"].search(password):
        #     raise ValueError("Пароль должен содержать хотя бы один спецсимвол (!@#$%^&* и т. д.)")
