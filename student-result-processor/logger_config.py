"""
logger_config.py
----------------
Central logging setup, shared by the whole package. Every error is
logged here instead of stopping the program, so processing can
continue with the next student.
"""

import logging
import os

LOG_FILE_NAME = "student_results.log"


def setup_logger(log_dir="."):
    log_path = os.path.join(log_dir, LOG_FILE_NAME)

    logger = logging.getLogger("student_result")
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