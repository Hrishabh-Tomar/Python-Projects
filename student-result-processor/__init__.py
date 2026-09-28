"""
student_result
---------------
A small package that validates student records (name, roll number,
5 subject marks) and calculates total, percentage, grade, and
pass/fail status.
"""

from .student import Student, build_student, SUBJECT_NAMES, NUM_SUBJECTS
from .result_calculator import calculate_result
from .logger_config import setup_logger
from .exceptions import (
    StudentResultError,
    InvalidMarksError,
    MissingStudentInfoError,
    ResultCalculationError,
)

__all__ = [
    "Student", "build_student", "SUBJECT_NAMES", "NUM_SUBJECTS",
    "calculate_result",
    "setup_logger",
    "StudentResultError", "InvalidMarksError", "MissingStudentInfoError",
    "ResultCalculationError",
]

__version__ = "1.0.0"