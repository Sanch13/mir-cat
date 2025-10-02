from typing import Any


class AppError(Exception):
    """
    Base application-level exception to provide consistent error handling.

    Attributes:
        message (str): Human-readable error message.
        context (Exception | None): Optional exception that caused the current error.

    """

    DEFAULT_MESSAGE = "Application error occurred."

    def __init__(self, message: str | None = None, context: Exception | None = None) -> None:
        """
        Initialize the AppError.

        Args:
            message: The error message.
            context: The context of the error.
        """
        self.message = message or self.DEFAULT_MESSAGE
        self.context = context
        super().__init__(self.message, self.context)
        if context:
            self.__cause__ = context

    def __str__(self) -> str:
        """Returns a string representation of the AppError."""
        if self.context:
            return f"{self.message} (caused by {self.context})"
        return self.message


class TemplateAppError(AppError):
    """
    TemplateAppError is a subclass of AppError that allows for dynamic error messages.

    Attributes:
        MESSAGE_TEMPLATE (str): The template for the error message.
        message (str): The error message.
        context (Exception | None): The context of the error.
        message_to_extend (dict[str, Any] | None): The keyword arguments for the error message.
    """

    MESSAGE_TEMPLATE: str | None = None

    def __init__(
        self,
        message: str | None = None,
        context: Exception | None = None,
        message_to_extend: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize the TemplateAppError.

        Args:
            message: The error message.
            context: The context of the error.
            message_to_extend: The keyword arguments for the error message.
        """
        if message is None and self.MESSAGE_TEMPLATE is not None:
            message = (
                self.MESSAGE_TEMPLATE.format(**message_to_extend)
                if message_to_extend is not None
                else self.MESSAGE_TEMPLATE
            )
        super().__init__(message=message, context=context)
