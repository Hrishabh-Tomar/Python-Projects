"""Data model for a single expense."""

from datetime import datetime

from exceptions import InvalidExpenseError

VALID_CATEGORIES = {
    "food", "transport", "housing", "utilities", "entertainment",
    "health", "shopping", "education", "other",
}

DATE_FORMAT = "%Y-%m-%d"


class Expense:
    """Represents one expense entry."""

    __slots__ = ("id", "amount", "category", "description", "date")

    def __init__(self, id, amount, category, description, date):
        self.id = id
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.description = description or ""
        self.date = self._validate_date(date)

    @staticmethod
    def _validate_amount(amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise InvalidExpenseError(f"Amount must be a number, got {amount!r}", field="amount")
        if amount <= 0:
            raise InvalidExpenseError("Amount must be greater than zero.", field="amount")
        return round(amount, 2)

    @staticmethod
    def _validate_category(category):
        if not category or not isinstance(category, str):
            raise InvalidExpenseError("Category is required.", field="category")
        category = category.strip().lower()
        if category not in VALID_CATEGORIES:
            raise InvalidExpenseError(
                f"Category must be one of {sorted(VALID_CATEGORIES)}, got {category!r}",
                field="category",
            )
        return category

    @staticmethod
    def _validate_date(date_str):
        try:
            datetime.strptime(date_str, DATE_FORMAT)
        except (TypeError, ValueError):
            raise InvalidExpenseError(
                f"Date must be in {DATE_FORMAT} format, got {date_str!r}", field="date"
            )
        return date_str

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data["date"],
        )

    def __repr__(self):
        return (
            f"Expense(id={self.id}, amount={self.amount}, category={self.category!r}, "
            f"description={self.description!r}, date={self.date!r})"
        )