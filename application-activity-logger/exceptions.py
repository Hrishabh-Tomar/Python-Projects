"""Custom exceptions for the menu-driven application."""


class AppError(Exception):
    """Base class for all application-specific errors."""


class AuthenticationError(AppError):
    """Raised when login/logout cannot be completed."""


class CalculationError(AppError):
    """Raised when a calculation cannot be completed."""


class FileOperationError(AppError):
    """Raised when a file read/write operation fails."""