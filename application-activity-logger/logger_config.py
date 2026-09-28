"""Central logging configuration for the whole application.

Two files are produced under logs/:
  - application.log : every record, DEBUG and above (the full trail)
  - error.log       : only ERROR and CRITICAL records (for quick triage)

WARNING and above are also echoed to the console so the user sees
problems immediately without having to open the log files.
"""

import logging
import os

LOG_DIR = "logs"
APPLICATION_LOG = os.path.join(LOG_DIR, "application.log")
ERROR_LOG = os.path.join(LOG_DIR, "error.log")

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

_configured = False


def setup_logging():
    """Configure the 'app' logger tree. Safe to call more than once."""
    global _configured
    root = logging.getLogger("app")

    if _configured:
        return root

    os.makedirs(LOG_DIR, exist_ok=True)
    formatter = logging.Formatter(_LOG_FORMAT)

    root.setLevel(logging.DEBUG)

    application_handler = logging.FileHandler(APPLICATION_LOG, encoding="utf-8")
    application_handler.setLevel(logging.DEBUG)
    application_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    root.addHandler(application_handler)
    root.addHandler(error_handler)
    root.addHandler(console_handler)

    _configured = True
    return root


def get_logger(name):
    """Return a named child logger, e.g. get_logger('auth') -> 'app.auth'."""
    setup_logging()
    return logging.getLogger(f"app.{name}")