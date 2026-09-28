"""
logger.py
---------
Central logging setup. Every successful and failed operation gets
written to a log file (and echoed to the console).
"""

import logging
import os

LOG_FILE_NAME = "file_organizer.log"


def setup_logger(log_dir="."):
    log_path = os.path.join(log_dir, LOG_FILE_NAME)

    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_success(logger, filename, destination_path):
    logger.info(f"SUCCESS | Moved '{filename}' -> '{destination_path}'")


def log_failure(logger, filename, reason):
    logger.error(f"FAILED  | '{filename}' -> {reason}")