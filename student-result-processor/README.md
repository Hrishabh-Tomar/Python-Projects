# Fault-Tolerant Student Result Processor

Python project that processes student marks for five subjects and calculates totals, percentages, grades, and pass/fail status.

## Planned structure

- `student_result_processor/` — Python package for student and result modules
- `main.py` — application entry point
- `logs/` — processing and error logs
- `tests/` — test files

## Requirements

- Separate student operations, result calculation, exception definitions, and logging modules
- Custom `InvalidMarksError` exception
- Continue processing students after invalid input or calculation errors
