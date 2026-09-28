"""JSON file-backed storage for expenses."""

import json
import os

from exceptions import StorageError
from logger_config import get_logger
from models import Expense

logger = get_logger("storage")

DEFAULT_DATA_FILE = os.path.join("data", "expenses.json")


class JsonStorage:
    """Reads and writes the list of expenses to a JSON file."""

    def __init__(self, file_path=DEFAULT_DATA_FILE):
        self.file_path = file_path
        data_dir = os.path.dirname(self.file_path)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)

    def load(self):
        """Return a list of Expense objects, or [] if the file doesn't exist yet."""
        if not os.path.exists(self.file_path):
            logger.info("Data file %s not found; starting with an empty list.", self.file_path)
            return []

        handle = None
        try:
            handle = open(self.file_path, "r", encoding="utf-8")
            raw = json.load(handle)
            expenses = [Expense.from_dict(item) for item in raw]
            logger.info("Loaded %d expenses from %s", len(expenses), self.file_path)
            return expenses
        except json.JSONDecodeError as exc:
            logger.error("Corrupt JSON in %s: %s", self.file_path, exc)
            raise StorageError(f"Data file {self.file_path} is corrupted: {exc}") from exc
        except OSError as exc:
            logger.error("Could not read %s: %s", self.file_path, exc)
            raise StorageError(f"Could not read data file {self.file_path}: {exc}") from exc
        finally:
            if handle is not None:
                handle.close()
                logger.debug("Closed handle for %s", self.file_path)

    def save(self, expenses):
        """Write the list of Expense objects to the JSON file."""
        handle = None
        try:
            handle = open(self.file_path, "w", encoding="utf-8")
            json.dump([e.to_dict() for e in expenses], handle, indent=2)
            logger.info("Saved %d expenses to %s", len(expenses), self.file_path)
        except OSError as exc:
            logger.error("Could not write %s: %s", self.file_path, exc)
            raise StorageError(f"Could not write data file {self.file_path}: {exc}") from exc
        finally:
            if handle is not None:
                handle.close()
                logger.debug("Closed handle for %s", self.file_path)