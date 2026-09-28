# Fault-Tolerant Student Result Processor

Processes student marks for five subjects and calculates totals, percentages, grades, and pass/fail status. Invalid records are logged while valid records continue processing.

## Usage

Run from this directory:

```powershell
python main.py
```

## Project Structure

- `main.py` - application entry point and batch processing
- `student.py` - student data validation
- `result_calculator.py` - totals, percentages, grades, and status
- `exceptions.py` - custom validation and calculation errors
- `logger_config.py` - console and file logging
