#!/usr/bin/env python3
"""A simple CLI calculator."""

import sys


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


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


def repl():
    """Run an interactive calculator loop."""
    print("Calculator — enter expressions like '2 + 3', or 'quit' to exit.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line or line in ("quit", "exit", "q"):
            break

        try:
            result = evaluate(line)
            print(result)
        except ValueError as e:
            print(f"Error: {e}")


def main():
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        try:
            print(evaluate(expression))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        repl()


if __name__ == "__main__":
    main()
