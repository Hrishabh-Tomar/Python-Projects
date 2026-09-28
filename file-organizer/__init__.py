"""
file_organizer
---------------
A small package that organizes files in a folder into subfolders
based on their extensions (e.g. photo.jpg -> Images/).
"""

from .detector import detect_category, is_supported, get_extension, EXTENSION_MAP
from .mover import move_file, ensure_destination_exists, resolve_duplicate_path
from .logger import setup_logger, log_success, log_failure
from .exceptions import (
    FileOrganizerError,
    UnsupportedFileError,
    FileNotFoundInSourceError,
    DestinationNotFoundError,
    DuplicateFileError,
)

__all__ = [
    "detect_category", "is_supported", "get_extension", "EXTENSION_MAP",
    "move_file", "ensure_destination_exists", "resolve_duplicate_path",
    "setup_logger", "log_success", "log_failure",
    "FileOrganizerError", "UnsupportedFileError", "FileNotFoundInSourceError",
    "DestinationNotFoundError", "DuplicateFileError",
]

__version__ = "1.0.0"