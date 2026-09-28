"""
mover.py
--------
Handles the actual filesystem work: creating destination folders,
handling duplicate filenames, and moving files with clear errors.
"""

import os
import shutil

from .exceptions import FileNotFoundInSourceError, DestinationNotFoundError


def ensure_destination_exists(destination_folder):
    if os.path.isdir(destination_folder):
        return
    try:
        os.makedirs(destination_folder, exist_ok=True)
    except OSError as e:
        raise DestinationNotFoundError(destination_folder) from e


def resolve_duplicate_path(destination_path):
    """
    'Images/photo.jpg' -> 'Images/photo (1).jpg' -> 'Images/photo (2).jpg' ...
    """
    if not os.path.exists(destination_path):
        return destination_path

    folder, filename = os.path.split(destination_path)
    name, ext = os.path.splitext(filename)

    counter = 1
    while True:
        new_filename = f"{name} ({counter}){ext}"
        new_path = os.path.join(folder, new_filename)
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def move_file(source_path, destination_folder, avoid_overwrite=True):
    if not os.path.isfile(source_path):
        raise FileNotFoundInSourceError(source_path)

    ensure_destination_exists(destination_folder)

    filename = os.path.basename(source_path)
    destination_path = os.path.join(destination_folder, filename)

    if avoid_overwrite:
        destination_path = resolve_duplicate_path(destination_path)

    shutil.move(source_path, destination_path)  # PermissionError propagates naturally

    return destination_path