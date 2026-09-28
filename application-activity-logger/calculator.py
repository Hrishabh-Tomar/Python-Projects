"""Calculator operation."""

from exceptions import CalculationError
from logger_config import get_logger

logger = get_logger("calculator")

_OPERATORS = {"+", "-", "*", "/"}


def calculate(raw_a, operator, raw_b):
    """Calculate raw_a <operator> raw_b, returning a float.

    Never lets ValueError/ZeroDivisionError escape -- always raises
    CalculationError instead.
    """
    logger.debug("Calculate requested: %r %r %r", raw_a, operator, raw_b)

    if operator not in _OPERATORS:
        logger.error("Unsupported operator: %r", operator)
        raise CalculationError(f"Unsupported operator {operator!r}. Use one of {sorted(_OPERATORS)}.")

    try:
        a = float(raw_a)
        b = float(raw_b)
    except (TypeError, ValueError) as exc:
        logger.error("Invalid numeric input: a=%r b=%r (%s)", raw_a, raw_b, exc)
        raise CalculationError("Both values must be numbers.") from exc

    try:
        if operator == "+":
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator == "*":
            result = a * b
        else:  # "/"
            result = a / b
    except ZeroDivisionError as exc:
        logger.error("Division by zero attempted: %s / %s", a, b)
        raise CalculationError("Cannot divide by zero.") from exc

    logger.info("Calculation completed: %s %s %s = %s", a, operator, b, result)
    return result