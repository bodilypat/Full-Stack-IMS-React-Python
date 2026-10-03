# app/core/exceptions.py

class AppException(Exception):
    """Base class for application errors with a stable error code."""

    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
    ):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self) -> dict[str, str]:
        """Return a consistent, serializable representation of the error."""
        return {"code": self.code, "message": self.message}

class NotFoundException(AppException):
    """Raised when a requested inventory resource does not exist."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            code="NOT_FOUND",
        )

class ConflictException(AppException):
    """Raised when an operation conflicts with existing inventory data."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            message=message,
            code="CONFLICT",
        )

class InsufficientStockException(AppException):
    """Raised when available stock cannot fulfill a requested quantity."""

    def __init__(self, message: str = "Insufficient stock"):
        super().__init__(
            message=message,
            code="INSUFFICIENT_STOCK",
        )
