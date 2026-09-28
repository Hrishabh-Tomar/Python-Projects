"""Core business logic for managing expenses."""

from collections import defaultdict

from exceptions import ExpenseNotFoundError
from logger_config import get_logger
from models import Expense
from storage import JsonStorage

logger = get_logger("tracker")


class ExpenseTracker:
    """In-memory expense list backed by JsonStorage."""

    def __init__(self, storage=None):
        self.storage = storage or JsonStorage()
        self.expenses = self.storage.load()
        self._next_id = (max((e.id for e in self.expenses), default=0)) + 1

    def add_expense(self, amount, category, description, date):
        expense = Expense(self._next_id, amount, category, description, date)
        self.expenses.append(expense)
        self._next_id += 1
        self.storage.save(self.expenses)
        logger.info("Added expense %s", expense)
        return expense

    def delete_expense(self, expense_id):
        for i, e in enumerate(self.expenses):
            if e.id == expense_id:
                removed = self.expenses.pop(i)
                self.storage.save(self.expenses)
                logger.info("Deleted expense %s", removed)
                return removed
        logger.warning("Attempted to delete missing expense id=%s", expense_id)
        raise ExpenseNotFoundError(expense_id)

    def list_expenses(self, category=None):
        result = self.expenses
        if category:
            category = category.strip().lower()
            result = [e for e in result if e.category == category]
        return sorted(result, key=lambda e: e.date)

    def total_by_category(self):
        totals = defaultdict(float)
        for e in self.expenses:
            totals[e.category] += e.amount
        return dict(sorted(totals.items(), key=lambda kv: -kv[1]))

    def total(self):
        return round(sum(e.amount for e in self.expenses), 2)