"""
exceptions.py
-------------
Custom exceptions for the file_organizer package.
"""


class FileOrganizerError(Exception):
    """Base class for all custom exceptions in this package."""
    pass


class UnsupportedFileError(FileOrganizerError):
    """Raised when a file's extension has no known destination category."""

    def __init__(self, filename, extension):
        self.filename = filename
        self.extension = extension
        super().__init__(
            f"Unsupported file type '{extension}' for file: {filename}"
        )


class FileNotFoundInSourceError(FileOrganizerError):
    """Raised when the file we were asked to move does not actually exist."""

    def __init__(self, filepath):
        self.filepath = filepath
        super().__init__(f"File not found: {filepath}")


class DestinationNotFoundError(FileOrganizerError):
    """Raised when the destination folder does not exist and could not be created."""

    def __init__(self, destination):
        self.destination = destination
        super().__init__(f"Destination folder missing/could not be created: {destination}")


class DuplicateFileError(FileOrganizerError):
    """Raised (informationally) when a file with the same name already exists
    at the destination and we choose not to silently overwrite it."""

    def __init__(self, filepath):
        self.filepath = filepath
        super().__init__(f"A file with this name already exists at destination: {filepath}")