"""
result_calculator.py
---------------------
Responsible for ONE job: turning a validated Student's marks into a
total, percentage, grade, and pass/fail status.
"""

from exceptions import ResultCalculationError

PASS_MARK_PER_SUBJECT = 33   # must score at least this much in EACH subject
PASS_PERCENTAGE = 40         # and at least this overall percentage


def calculate_total(marks):
    return sum(marks)


def calculate_percentage(total, num_subjects):
    if num_subjects == 0:
        raise ResultCalculationError("unknown", "cannot divide by zero subjects")
    return total / num_subjects


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 75:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 40:
        return "C"
    else:
        return "F"


def calculate_pass_fail(marks, percentage):
    failed_a_subject = any(mark < PASS_MARK_PER_SUBJECT for mark in marks)
    below_overall = percentage < PASS_PERCENTAGE
    return "FAIL" if (failed_a_subject or below_overall) else "PASS"


def calculate_result(student):
    """
    Given a validated Student object, return a dict with:
        total, percentage, grade, status
    """
    try:
        marks = student.marks
        num_subjects = len(marks)

        total = calculate_total(marks)
        percentage = calculate_percentage(total, num_subjects)
        grade = calculate_grade(percentage)
        status = calculate_pass_fail(marks, percentage)

        return {
            "name": student.name,
            "roll_no": student.roll_no,
            "total": total,
            "percentage": round(percentage, 2),
            "grade": grade,
            "status": status,
        }

    except ZeroDivisionError as e:
        raise ResultCalculationError(student.name, f"division error: {e}")
    except Exception as e:
        raise ResultCalculationError(student.name, f"unexpected error: {e}")