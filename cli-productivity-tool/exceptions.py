"""Custom exceptions for the Personal Expense Tracker."""


class ExpenseTrackerError(Exception):
    """Base class for all expense tracker errors."""


class InvalidExpenseError(ExpenseTrackerError):
    """Raised when expense data (amount, category, date) is invalid."""

    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field


class ExpenseNotFoundError(ExpenseTrackerError):
    """Raised when an expense id does not exist."""

    def __init__(self, expense_id):
        super().__init__(f"Expense with id {expense_id} was not found.")
        self.expense_id = expense_id


class StorageError(ExpenseTrackerError):
    """Raised when reading or writing the data file fails."""