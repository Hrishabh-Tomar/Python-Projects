"""
main.py
-------
Entry point. Scans a source folder, detects each file's category,
moves it, and logs the outcome.

Usage:
    python -m File_Organizer /path/to/folder
    python -m File_Organizer  (defaults to ./sample_files)
"""

import os
import sys

from . import (
    detect_category,
    move_file,
    setup_logger,
    log_success,
    log_failure,
    UnsupportedFileError,
    FileNotFoundInSourceError,
    DestinationNotFoundError,
)


def organize_folder(source_folder, logger):
    if not os.path.isdir(source_folder):
        logger.error(f"FAILED  | Source folder does not exist: {source_folder}")
        return

    entries = os.listdir(source_folder)
    files = [f for f in entries if os.path.isfile(os.path.join(source_folder, f))]

    if not files:
        logger.info(f"No files found to organize in: {source_folder}")
        return

    for filename in files:
        source_path = os.path.join(source_folder, filename)

        try:
            category = detect_category(filename)
            destination_folder = os.path.join(source_folder, category)
            final_path = move_file(source_path, destination_folder)
            log_success(logger, filename, final_path)

        except UnsupportedFileError as e:
            log_failure(logger, filename, f"Unsupported file type ({e.extension})")

        except FileNotFoundInSourceError as e:
            log_failure(logger, filename, f"File not found: {e.filepath}")

        except DestinationNotFoundError as e:
            log_failure(logger, filename, f"Destination folder unavailable: {e.destination}")

        except PermissionError as e:
            log_failure(logger, filename, f"Permission denied: {e}")

        except Exception as e:
            log_failure(logger, filename, f"Unexpected error: {e}")


def main():
    source_folder = sys.argv[1] if len(sys.argv) > 1 else "sample_files"

    logger = setup_logger(log_dir=".")
    logger.info(f"=== Starting file organization for: {source_folder} ===")

    organize_folder(source_folder, logger)

    logger.info("=== File organization complete ===")


if __name__ == "__main__":
    main()