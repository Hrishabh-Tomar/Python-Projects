"""Logging setup: all application logs go to a file."""

import logging
import os

LOG_FILE = os.path.join("logs", "expense_tracker.log")


def setup_logging(log_file=LOG_FILE, level=logging.INFO):
    """Configure the root 'expense_tracker' logger to write to a file."""
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("expense_tracker")
    logger.setLevel(level)

    # Avoid adding duplicate handlers if called more than once.
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)
    return logger


def get_logger(name):
    """Return a child logger, e.g. get_logger('storage')."""
    return logging.getLogger(f"expense_tracker.{name}")