from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.shared.exceptions import (
    FieldNegativeError,
    FieldTooLongError,
    FieldTooShortError,
    FieldZeroError,
    InvalidTypeError,
)


@dataclass(frozen=True)
class UuidVo:
    """
    UUID Value Object for validating and representing UUID values.

    This class ensures that the provided value is a valid UUID instance
    and provides type safety for UUID operations.

    Attributes:
        value (UUID): The UUID value to validate

    Raises:
        InvalidTypeError: If value is not a UUID instance
    """

    value: UUID

    def __post_init__(self):
        """
        Validate that the value is a UUID instance.

        Performs type checking to ensure the value is a proper UUID object
        and not a string or other type that might represent a UUID.
        """
        if not isinstance(self.value, UUID):
            raise InvalidTypeError(
                message_to_extend={
                    "expected_type": "UUID",
                    "attr_name": "value of UuidVo",
                    "actual_type": type(self.value).__name__,
                    "value": self.value,
                }
            )


@dataclass(frozen=True)
class IntVo:
    """
    Integer Value Object for validating and representing integer values.

    This class ensures that the provided value is a valid integer
    and provides type safety for integer operations.

    Attributes:
        value (int): The integer value to validate

    Raises:
        InvalidTypeError: If value is not an integer
    """

    value: int

    def __post_init__(self):
        """
        Validate that the value is an integer.

        Performs type checking to ensure the value is a proper integer
        and not a string or float that could be converted to integer.
        """
        if not isinstance(self.value, int):
            raise InvalidTypeError(
                message_to_extend={
                    "expected_type": "int",
                    "attr_name": "value of IntVo",
                    "actual_type": type(self.value).__name__,
                    "value": self.value,
                }
            )


@dataclass(frozen=True)
class PositiveIntVo(IntVo):
    def __post_init__(self):
        super().__post_init__()
        if self.value < 0:
            raise FieldNegativeError(
                message_to_extend={
                    "attr_name": "value of PositiveIntVo",
                    "value": self.value,
                }
            )
        elif self.value == 0:
            raise FieldZeroError(
                message_to_extend={
                    "attr_name": "value of PositiveIntVo",
                }
            )


@dataclass(frozen=True)
class DatetimeVo:
    """
    Datetime Value Object for validating and representing datetime values.

    This class ensures that the provided value is a valid datetime instance
    and provides type safety for datetime operations.

    Attributes:
        value (datetime): The datetime value to validate

    Raises:
        InvalidTypeError: If value is not a datetime instance
    """

    value: datetime

    def __post_init__(self):
        """
        Validate that the value is a datetime instance.

        Performs type checking to ensure the value is a proper datetime object
        and not a string or other datetime representation.
        """
        if not isinstance(self.value, datetime):
            raise InvalidTypeError(
                message_to_extend={
                    "expected_type": "datetime",
                    "attr_name": "value of DatetimeVo",
                    "actual_type": type(self.value).__name__,
                    "value": self.value,
                }
            )


@dataclass(frozen=True)
class StrVo:
    """
    String Value Object for validating and representing string values.

    This class ensures that the provided value is a valid string
    and serves as the base class for more specialized string VOs.

    Attributes:
        value (str): The string value to validate

    Raises:
        InvalidTypeError: If value is not a string
    """

    value: str

    def __post_init__(self):
        """
        Validate that the value is a string.

        Performs type checking to ensure the value is a proper string
        and not a number or other type that could be converted to string.
        """
        if not isinstance(self.value, str):
            raise InvalidTypeError(
                message_to_extend={
                    "expected_type": "str",
                    "attr_name": "value of StrVo",
                    "actual_type": type(self.value).__name__,
                    "value": self.value,
                }
            )


@dataclass(frozen=True)
class StrWithSizeVo(StrVo):
    """
    Base class for string Value Objects with size constraints.

    This class extends StrVo to add minimum and maximum length validation.
    Subclasses should define _MIN_SIZE and/or _MAX_SIZE class variables
    to enforce size constraints.

    Attributes:
        value (str): The string value to validate
        min_size (property): Returns the minimum allowed length
        max_size (property): Returns the maximum allowed length

    Raises:
        FieldTooShortError: If value length is less than min_size
        FieldTooLongError: If value length is greater than max_size
    """

    @property
    def min_size(self) -> int:
        """
        Get the minimum allowed string length.

        Returns:
            int: Minimum size constraint or None if not set

        Note:
            Uses getattr() to safely retrieve _MIN_SIZE from subclass.
            Returns None if _MIN_SIZE is not defined.
        """
        return getattr(self, "MIN_SIZE", None)

    @property
    def max_size(self) -> int:
        """
        Get the maximum allowed string length.

        Returns:
            int: Maximum size constraint or None if not set

        Note:
            Uses getattr() to safely retrieve _MAX_SIZE from subclass.
            Returns None if _MAX_SIZE is not defined.
        """
        return getattr(self, "MAX_SIZE", None)

    def __post_init__(self):
        """
        Validate string size constraints after initialization.

        Performs the following validations:
        1. Calls parent class validation (type checking)
        2. Strips whitespace and calculates length
        3. Validates against min_size if set
        4. Validates against max_size if set

        The validation is lenient - constraints are only enforced
        if the corresponding _MIN_SIZE/_MAX_SIZE are defined.

        Raises:
            FieldTooShortError: When value is shorter than min_size
            FieldTooLongError: When value is longer than max_size
        """
        super().__post_init__()
        length = len(self.value.strip())

        # Validate minimum length if constraint is set
        if self.min_size is not None and length < self.min_size:
            raise FieldTooShortError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "min_length": self.min_size,
                    "current_length": length,
                    "value": self.value,
                }
            )

        # Validate maximum length if constraint is set
        elif self.max_size is not None and length > self.max_size:
            raise FieldTooLongError(
                message_to_extend={
                    "attr_name": self.__class__.__name__,
                    "max_length": self.max_size,
                    "current_length": length,
                    "value": self.value,
                }
            )
