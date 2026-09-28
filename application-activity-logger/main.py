#!/usr/bin/env python3
"""Menu-driven application demonstrating structured, multi-level logging.

Menu:
    1. Login
    2. Calculate
    3. Read a File
    4. Write a File
    5. Logout
    0. Exit

Every action is wrapped in its own try/except so a failure in one
operation (bad login, division by zero, a missing file, ...) never
terminates the whole application. A final catch-all in the main loop
logs CRITICAL for anything truly unexpected and keeps the menu running.
"""

from auth import Session, login, logout
from calculator import calculate
from exceptions import AppError
from file_ops import read_file, write_file
from logger_config import get_logger, setup_logging

logger = get_logger("main")

MENU = """
==== Menu ====
1. Login
2. Calculate
3. Read a File
4. Write a File
5. Logout
0. Exit
"""


def action_login(session):
    if session.is_logged_in:
        print(f"Already logged in as {session.username}.")
        return
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    try:
        login(session, username, password)
        print(f"Welcome, {username}!")
    except AppError as exc:
        print(f"Login failed: {exc}")


def action_calculate(session):
    if not session.is_logged_in:
        logger.warning("Calculate attempted without an active login")
        print("Please login first.")
        return
    a = input("First number: ").strip()
    op = input("Operator (+, -, *, /): ").strip()
    b = input("Second number: ").strip()
    try:
        result = calculate(a, op, b)
        print(f"Result: {result}")
    except AppError as exc:
        print(f"Calculation error: {exc}")


def action_read_file(session):
    if not session.is_logged_in:
        logger.warning("Read-file attempted without an active login")
        print("Please login first.")
        return
    path = input("File path to read: ").strip()
    try:
        content = read_file(path)
        print("--- File content ---")
        print(content if content.strip() else "(file is empty)")
    except AppError as exc:
        print(f"Could not read file: {exc}")


def action_write_file(session):
    if not session.is_logged_in:
        logger.warning("Write-file attempted without an active login")
        print("Please login first.")
        return
    path = input("File path to write: ").strip()
    content = input("Content to write: ")
    try:
        write_file(path, content)
        print("File written successfully.")
    except AppError as exc:
        print(f"Could not write file: {exc}")


def action_logout(session):
    try:
        logout(session)
        print("Logged out successfully.")
    except AppError as exc:
        print(f"Logout failed: {exc}")


ACTIONS = {
    "1": action_login,
    "2": action_calculate,
    "3": action_read_file,
    "4": action_write_file,
    "5": action_logout,
}


def main():
    setup_logging()
    logger.info("Application started")
    session = Session()

    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()

            if choice == "0":
                logger.info("Application exiting normally")
                print("Goodbye!")
                break

            action = ACTIONS.get(choice)
            if action is None:
                logger.debug("Invalid menu choice entered: %r", choice)
                print("Invalid choice, try again.")
                continue

            try:
                action(session)
            except AppError as exc:
                logger.error("Unhandled application error in option %s: %s", choice, exc)
                print(f"Error: {exc}")
            except Exception:
                logger.critical(
                    "Unexpected application failure in option %s", choice, exc_info=True
                )
                print("An unexpected error occurred. It has been logged; the app will continue.")
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
        print("\nGoodbye!")


if __name__ == "__main__":
    main()