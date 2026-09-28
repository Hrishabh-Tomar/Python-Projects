# CLI Expense Tracker

A command-line tool for recording expenses, listing them, and displaying totals by category. Invalid input is handled with custom exceptions and application activity is logged.

## Usage

Run from this directory:

```powershell
python main.py add 45.50 food "Weekly groceries"
python main.py list
python main.py summary
```

Run the tests:

```powershell
python -m unittest test_expense_tracker.py -v
```

Supported categories include `food`, `transport`, `bills`, `shopping`, `health`, `entertainment`, and `other`.

## Project Structure

- `main.py` - command-line interface
- `tracker.py` - expense management operations
- `models.py` - expense validation and data model
- `storage.py` - JSON persistence
- `exceptions.py` - custom application errors
- `logger_config.py` - file and console logging
