"""
detector.py
-----------
Responsible for ONE job: figuring out what category a file belongs to,
based on its extension (e.g. .jpg -> "Images").
"""

import os

from .exceptions import UnsupportedFileError

EXTENSION_MAP = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images",
    ".txt": "Text", ".md": "Text", ".log": "Text",
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents", ".pptx": "Documents",
    ".csv": "Data", ".xlsx": "Data", ".json": "Data", ".xml": "Data",
    ".zip": "Archives", ".rar": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".mp3": "Audio", ".wav": "Audio",
    ".mp4": "Video", ".mov": "Video",
}


def get_extension(filename):
    return os.path.splitext(filename)[1].lower()


def detect_category(filename):
    extension = get_extension(filename)

    if extension == "":
        raise UnsupportedFileError(filename, "(no extension)")

    if extension not in EXTENSION_MAP:
        raise UnsupportedFileError(filename, extension)

    return EXTENSION_MAP[extension]


def is_supported(filename):
    try:
        detect_category(filename)
        return True
    except UnsupportedFileError:
        return False