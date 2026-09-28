# Application Activity Logger

A menu-driven Python application with login, calculation, file reading, file writing, and logout activities. Each action is logged and handled without terminating the application on expected errors.

## Usage

Run from this directory:

```powershell
python main.py
```

Demo login credentials:

- Username: `admin`
- Password: `admin123`

The menu supports login, arithmetic calculations, reading and writing text files, logout, and clean exit. Logs are written to the `logs` directory.

## Project Structure

- `main.py` - interactive application entry point
- `auth.py` - login session management
- `calculator.py` - arithmetic operations
- `file_ops.py` - text file operations
- `exceptions.py` - application-specific errors
- `logger_config.py` - console and file logging setup
