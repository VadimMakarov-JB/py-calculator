#!/usr/bin/env python3
"""A simple CLI calculator."""

import sys

from evaluator import evaluate


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
