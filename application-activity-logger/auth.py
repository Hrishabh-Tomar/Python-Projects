"""Login / logout handling."""

from exceptions import AuthenticationError
from logger_config import get_logger

logger = get_logger("auth")

_USERS = {
    "admin": "admin123",
    "hrishabh": "password1",
}


class Session:
    """Tracks whether a user is currently logged in."""

    def __init__(self):
        self.username = None

    @property
    def is_logged_in(self):
        return self.username is not None


def login(session, username, password):
    logger.debug("Login attempt for username=%r", username)

    if not username or not password:
        logger.warning("Login attempt with missing username or password")
        raise AuthenticationError("Username and password are required.")

    if session.is_logged_in:
        logger.warning("Login attempted while already logged in as %s", session.username)
        raise AuthenticationError(f"Already logged in as {session.username}.")

    expected_password = _USERS.get(username)
    if expected_password is None or expected_password != password:
        logger.warning("Failed login attempt for username=%r", username)
        raise AuthenticationError("Invalid username or password.")

    session.username = username
    logger.info("User logged in: %s", username)


def logout(session):
    if not session.is_logged_in:
        logger.warning("Logout attempted with no active session")
        raise AuthenticationError("No user is currently logged in.")

    logger.info("User logged out: %s", session.username)
    session.username = None