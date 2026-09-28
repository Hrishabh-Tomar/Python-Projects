"""Read / write file operations."""

import os

from exceptions import FileOperationError
from logger_config import get_logger

logger = get_logger("file_ops")


def read_file(path):
    """Return the text content of path, or raise FileOperationError."""
    logger.debug("Attempting to read file: %s", path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError as exc:
        logger.error("File could not be opened (not found): %s", path)
        raise FileOperationError(f"File not found: {path}") from exc
    except PermissionError as exc:
        logger.error("File could not be opened (permission denied): %s", path)
        raise FileOperationError(f"Permission denied: {path}") from exc
    except OSError as exc:
        logger.error("File could not be opened: %s (%s)", path, exc)
        raise FileOperationError(f"Could not open file {path}: {exc}") from exc

    if content.strip() == "":
        logger.warning("File was empty: %s", path)
    else:
        logger.info("File read successfully: %s (%d characters)", path, len(content))

    return content


def write_file(path, content):
    """Write content to path, creating parent directories as needed."""
    logger.debug("Attempting to write file: %s", path)

    if content.strip() == "":
        logger.warning("Writing empty content to file: %s", path)

    directory = os.path.dirname(path)
    try:
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except PermissionError as exc:
        logger.error("File could not be written (permission denied): %s", path)
        raise FileOperationError(f"Permission denied: {path}") from exc
    except OSError as exc:
        logger.error("File could not be written: %s (%s)", path, exc)
        raise FileOperationError(f"Could not write file {path}: {exc}") from exc

    logger.info("File written successfully: %s (%d characters)", path, len(content))