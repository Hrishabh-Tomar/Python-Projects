"""Basic tests for the Personal Expense Tracker (run with: python3 test_expense_tracker.py)."""

import os
import shutil
import unittest

from exceptions import ExpenseNotFoundError, InvalidExpenseError, StorageError
from models import Expense
from storage import JsonStorage
from tracker import ExpenseTracker

TEST_DIR = "test_data_tmp"
TEST_FILE = os.path.join(TEST_DIR, "expenses.json")


class ExpenseModelTests(unittest.TestCase):
    def test_valid_expense(self):
        e = Expense(1, "10.5", "Food", "Lunch", "2026-09-01")
        self.assertEqual(e.amount, 10.5)
        self.assertEqual(e.category, "food")

    def test_negative_amount_rejected(self):
        with self.assertRaises(InvalidExpenseError):
            Expense(1, -5, "food", "x", "2026-09-01")

    def test_invalid_category_rejected(self):
        with self.assertRaises(InvalidExpenseError):
            Expense(1, 5, "not_a_category", "x", "2026-09-01")

    def test_invalid_date_rejected(self):
        with self.assertRaises(InvalidExpenseError):
            Expense(1, 5, "food", "x", "09/01/2026")


class StorageTests(unittest.TestCase):
    def setUp(self):
        os.makedirs(TEST_DIR, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_DIR, ignore_errors=True)

    def test_round_trip(self):
        store = JsonStorage(TEST_FILE)
        expenses = [Expense(1, 10, "food", "a", "2026-09-01")]
        store.save(expenses)
        loaded = store.load()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].amount, 10)

    def test_corrupted_file_raises_storage_error(self):
        with open(TEST_FILE, "w") as f:
            f.write("{bad json")
        store = JsonStorage(TEST_FILE)
        with self.assertRaises(StorageError):
            store.load()

    def test_missing_file_returns_empty_list(self):
        store = JsonStorage(TEST_FILE)
        self.assertEqual(store.load(), [])


class TrackerTests(unittest.TestCase):
    def setUp(self):
        os.makedirs(TEST_DIR, exist_ok=True)
        self.tracker = ExpenseTracker(JsonStorage(TEST_FILE))

    def tearDown(self):
        shutil.rmtree(TEST_DIR, ignore_errors=True)

    def test_add_and_list(self):
        self.tracker.add_expense(20, "food", "Groceries", "2026-09-05")
        self.tracker.add_expense(10, "transport", "Bus", "2026-09-01")
        result = self.tracker.list_expenses()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].date, "2026-09-01")  # sorted by date

    def test_delete_existing(self):
        e = self.tracker.add_expense(20, "food", "Groceries", "2026-09-05")
        removed = self.tracker.delete_expense(e.id)
        self.assertEqual(removed.id, e.id)
        self.assertEqual(self.tracker.list_expenses(), [])

    def test_delete_missing_raises(self):
        with self.assertRaises(ExpenseNotFoundError):
            self.tracker.delete_expense(999)

    def test_totals(self):
        self.tracker.add_expense(20, "food", "a", "2026-09-01")
        self.tracker.add_expense(30, "food", "b", "2026-09-02")
        self.tracker.add_expense(5, "transport", "c", "2026-09-03")
        totals = self.tracker.total_by_category()
        self.assertEqual(totals["food"], 50)
        self.assertEqual(self.tracker.total(), 55)


if __name__ == "__main__":
    unittest.main()