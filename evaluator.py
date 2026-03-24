"""Expression parsing and evaluation."""

from operations import OPERATIONS


def evaluate(expression: str) -> float:
    """Evaluate a simple 'number operator number' expression."""
    parts = expression.split()
    if len(parts) != 3:
        raise ValueError("Expected format: <number> <operator> <number>")

    a_str, op, b_str = parts

    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        raise ValueError(f"Invalid number in expression: {expression}")

    if op not in OPERATIONS:
        raise ValueError(f"Unknown operator '{op}'. Supported: {', '.join(OPERATIONS)}")

    return OPERATIONS[op](a, b)
