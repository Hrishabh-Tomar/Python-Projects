"""
main.py
-------
Entry point. Processes a batch of raw student records, logs every
success/failure, and continues instead of crashing on bad data.
"""

from student import build_student
from result_calculator import calculate_result
from logger_config import setup_logger
from exceptions import (
    InvalidMarksError,
    MissingStudentInfoError,
    ResultCalculationError,
)

RAW_STUDENT_RECORDS = [
    {"name": "Asha Patel",   "roll_no": "101", "marks": [88, 92, 76, 65, 81]},   # valid
    {"name": "Ravi Kumar",   "roll_no": "102", "marks": [45, 39, 50, 60, 55]},   # valid
    {"name": "Meena Rao",    "roll_no": "103", "marks": [70, "abc", 60, 80, 90]}, # non-numeric mark
    {"name": "John Smith",   "roll_no": "104", "marks": [110, 90, 85, 70, 60]},  # out of range (>100)
    {"name": "",             "roll_no": "105", "marks": [70, 65, 60, 55, 50]},   # missing name
    {"name": "Priya Singh",  "roll_no": "106", "marks": [-5, 60, 70, 80, 90]},   # out of range (<0)
    {"name": "Karan Mehta",  "roll_no": "107", "marks": [70, 65, 60, 55]},       # wrong subject count
    {"name": "Sara Ali",     "roll_no": "108"},                                 # missing marks
    {"name": "David Lee",    "roll_no": "109", "marks": [95, 88, 92, 79, 84]},   # valid
]


def process_students(raw_records, logger):
    results = []

    for record in raw_records:
        student_label = record.get("name") or record.get("roll_no", "UNKNOWN")

        try:
            student = build_student(record)
            result = calculate_result(student)

            logger.info(
                f"SUCCESS | {result['name']} (Roll {result['roll_no']}) -> "
                f"Total={result['total']}, %={result['percentage']}, "
                f"Grade={result['grade']}, Status={result['status']}"
            )
            results.append(result)

        except MissingStudentInfoError as e:
            logger.error(f"FAILED  | {student_label} -> Missing info: {e}")

        except InvalidMarksError as e:
            logger.error(f"FAILED  | {student_label} -> Invalid marks: {e}")

        except ResultCalculationError as e:
            logger.error(f"FAILED  | {student_label} -> Calculation error: {e}")

        except Exception as e:
            logger.error(f"FAILED  | {student_label} -> Unexpected error: {e}")

    return results


def print_summary(results):
    print("\n" + "=" * 70)
    print(f"{'Name':<15}{'Roll':<8}{'Total':<8}{'%':<8}{'Grade':<8}{'Status':<8}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<15}{r['roll_no']:<8}{r['total']:<8}{r['percentage']:<8}{r['grade']:<8}{r['status']:<8}")
    print("=" * 70)
    print(f"Processed successfully: {len(results)} / {len(RAW_STUDENT_RECORDS)}")


def main():
    logger = setup_logger(log_dir=".")
    logger.info("=== Starting student result processing ===")

    results = process_students(RAW_STUDENT_RECORDS, logger)

    logger.info(f"=== Finished. {len(results)}/{len(RAW_STUDENT_RECORDS)} students processed successfully ===")

    print_summary(results)


if __name__ == "__main__":
    main()