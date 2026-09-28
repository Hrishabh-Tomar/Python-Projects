"""
exceptions.py
-------------
Custom exceptions for the student_result package.
"""


class StudentResultError(Exception):
    """Base class for all custom exceptions in this package."""
    pass


class InvalidMarksError(StudentResultError):
    """
    Raised when a mark is non-numeric, missing, or outside the valid
    0-100 range.
    """

    def __init__(self, student_name, subject, value, reason=None):
        self.student_name = student_name
        self.subject = subject
        self.value = value
        if reason is None:
            reason = "must be a number between 0 and 100"
        super().__init__(
            f"Invalid marks for {student_name} in {subject}: {value!r} ({reason})"
        )


class MissingStudentInfoError(StudentResultError):
    """Raised when required student information (name, roll no, marks list) is missing."""

    def __init__(self, field_name, record):
        self.field_name = field_name
        self.record = record
        super().__init__(f"Missing required field '{field_name}' in record: {record}")


class ResultCalculationError(StudentResultError):
    """Raised when total/percentage/grade calculation fails unexpectedly
    (e.g. wrong number of subjects, division error)."""

    def __init__(self, student_name, reason):
        self.student_name = student_name
        self.reason = reason
        super().__init__(f"Could not calculate result for {student_name}: {reason}")