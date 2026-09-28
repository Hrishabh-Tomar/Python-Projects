"""
student.py
----------
Responsible for ONE job: representing a student and validating their
raw input data (name, roll number, and 5 subject marks) before any
calculation happens.
"""

from exceptions import InvalidMarksError, MissingStudentInfoError

REQUIRED_FIELDS = ["name", "roll_no", "marks"]
NUM_SUBJECTS = 5
SUBJECT_NAMES = ["Math", "Science", "English", "History", "Computer"]


class Student:
    """A validated student record, ready for result calculation."""

    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks  # list of 5 floats, guaranteed valid at this point

    def __repr__(self):
        return f"Student(name={self.name!r}, roll_no={self.roll_no!r}, marks={self.marks})"


def _to_number(value):
    """Convert value to float, raising ValueError if it's not numeric."""
    if isinstance(value, bool):
        raise ValueError(f"Boolean is not a valid mark: {value!r}")
    return float(value)


def build_student(record):
    """
    Validate a raw student record (usually a dict from a CSV row, form
    input, etc.) and return a Student object.

    record example:
        {"name": "Asha", "roll_no": "101", "marks": [88, 92, 76, 65, 81]}

    Raises:
        MissingStudentInfoError - if name, roll_no, or marks is missing
        InvalidMarksError       - if a mark is non-numeric or outside 0-100,
                                   or the wrong number of marks is given
    """
    for field in REQUIRED_FIELDS:
        if field not in record or record[field] in (None, ""):
            raise MissingStudentInfoError(field, record)

    name = record["name"]
    roll_no = record["roll_no"]
    raw_marks = record["marks"]

    if not isinstance(raw_marks, (list, tuple)):
        raise MissingStudentInfoError("marks (must be a list)", record)

    if len(raw_marks) != NUM_SUBJECTS:
        raise InvalidMarksError(
            name, "subject count", len(raw_marks),
            reason=f"expected {NUM_SUBJECTS} marks"
        )

    validated_marks = []
    for subject, raw_value in zip(SUBJECT_NAMES, raw_marks):
        try:
            value = _to_number(raw_value)
        except (ValueError, TypeError):
            raise InvalidMarksError(name, subject, raw_value)

        if value < 0 or value > 100:
            raise InvalidMarksError(name, subject, raw_value)

        validated_marks.append(value)

    return Student(name=name, roll_no=roll_no, marks=validated_marks)