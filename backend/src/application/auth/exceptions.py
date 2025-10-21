from src.application.base_exception import ApplicationError


class UnauthorizedError(ApplicationError):
    DEFAULT_MESSAGE = "Invalid username or password"
