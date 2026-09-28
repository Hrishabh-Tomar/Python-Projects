# Application Activity Logger

Menu-driven Python application with login, calculation, file reading, file writing, and logout activities.

## Planned structure

- `activity_logger/` — Python package for application modules
- `main.py` — application entry point
- `logs/application.log` — DEBUG, INFO, WARNING, ERROR, and CRITICAL logs
- `logs/error.log` — error-focused logs
- `tests/` — test files

## Requirements

- Separate modules instead of placing all logic in `main.py`
- Continue running when an operation fails
- Generate all required logging levels
- Store logs in the `logs/` directory
