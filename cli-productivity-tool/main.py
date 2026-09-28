#!/usr/bin/env python3
"""Command-line entry point for the Personal Expense Tracker."""

import argparse
import sys
from datetime import date

from exceptions import ExpenseTrackerError
from logger_config import get_logger, setup_logging
from models import VALID_CATEGORIES
from tracker import ExpenseTracker

logger = get_logger("cli")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track personal expenses from the command line.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new expense")
    add_p.add_argument("amount", type=float, help="Expense amount, e.g. 12.50")
    add_p.add_argument("category", help=f"One of: {', '.join(sorted(VALID_CATEGORIES))}")
    add_p.add_argument("description", help="Short description of the expense")
    add_p.add_argument(
        "--date", default=date.today().isoformat(),
        help="Date in YYYY-MM-DD format (default: today)",
    )

    del_p = sub.add_parser("delete", help="Delete an expense by id")
    del_p.add_argument("id", type=int)

    list_p = sub.add_parser("list", help="List expenses")
    list_p.add_argument("--category", default=None, help="Filter by category")

    sub.add_parser("summary", help="Show totals per category and overall")

    return parser


def cmd_add(tracker, args):
    expense = tracker.add_expense(args.amount, args.category, args.description, args.date)
    print(f"Added expense #{expense.id}: {expense.amount:.2f} [{expense.category}] "
          f"{expense.description} on {expense.date}")


def cmd_delete(tracker, args):
    removed = tracker.delete_expense(args.id)
    print(f"Deleted expense #{removed.id}: {removed.amount:.2f} [{removed.category}] "
          f"{removed.description}")


def cmd_list(tracker, args):
    expenses = tracker.list_expenses(category=args.category)
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<4} {'Date':<12} {'Category':<14} {'Amount':>10}  Description")
    print("-" * 60)
    for e in expenses:
        print(f"{e.id:<4} {e.date:<12} {e.category:<14} {e.amount:>10.2f}  {e.description}")


def cmd_summary(tracker, args):
    totals = tracker.total_by_category()
    if not totals:
        print("No expenses recorded yet.")
        return
    print("Totals by category:")
    for cat, amount in totals.items():
        print(f"  {cat:<14} {amount:>10.2f}")
    print("-" * 26)
    print(f"  {'TOTAL':<14} {tracker.total():>10.2f}")


COMMANDS = {
    "add": cmd_add,
    "delete": cmd_delete,
    "list": cmd_list,
    "summary": cmd_summary,
}


def main(argv=None):
    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    handler = COMMANDS[args.command]

    try:
        tracker = ExpenseTracker()
        handler(tracker, args)
    except ExpenseTrackerError as exc:
        logger.error("%s command failed: %s", args.command, exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception:
        logger.exception("Unexpected error running command %s", args.command)
        print("An unexpected error occurred. See logs/expense_tracker.log for details.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())