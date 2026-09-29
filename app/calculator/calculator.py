"""Professional Calculator command loop."""

from __future__ import annotations

import math

from colorama import Fore, init

from app.calculation import Calculation, CalculationFactory, calculate, evaluate_expression
from app.operation import (
    INVALID_OPERATION_MESSAGE,
    OPERATION_ALIASES,
    OPERATION_SYMBOLS,
    VALID_OPERATIONS,
    add,
    divide,
    multiply,
    subtract,
)

init(autoreset=True)

OPERATION_COLORS = {
    "add": Fore.CYAN,
    "subtract": Fore.YELLOW,
    "multiply": Fore.MAGENTA,
    "divide": Fore.RED,
}


def _parse_number(raw_value: str, label: str) -> float:
    """Convert a user-entered number string into a float or raise a helpful error."""
    try:
        number = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"Invalid {label} number: {raw_value!r}. Please enter a valid number.") from exc

    if not math.isfinite(number):
        raise ValueError(f"Invalid {label} number: {raw_value!r}. Please enter a finite number.")
    return number


def _print_help() -> None:
    """Display the commands and arithmetic operations available in the REPL."""
    print("Commands: help, history, exit")
    print(
        "Operations: "
        + ", ".join(
            f"{name} ({OPERATION_SYMBOLS[name]})" for name in OPERATION_ALIASES
        )
    )
    print(
        "Aliases: "
        + ", ".join(
            alias
            for aliases in OPERATION_ALIASES.values()
            for alias in aliases[1:-1]
        )
    )


def _print_history(history: list[Calculation]) -> None:
    """Display successful calculations recorded during this session."""
    if not history:
        print("No calculations in history.")
        return

    for index, calculation in enumerate(history, start=1):
        result = calculation.calculate()
        print(
            f"{index}. {calculation.first_number} {calculation.symbol} "
            f"{calculation.second_number} = {result}"
        )


def run_interactive() -> None:
    """Run a simple Professional Calculator loop in the terminal."""
    history: list[Calculation] = []
    print("-------------------- Professional Calculator --------------------")
    print("Available operations: " + ", ".join(OPERATION_ALIASES))
    print("----------------------------------------------------------------")

    for operation_name, aliases in OPERATION_ALIASES.items():
        symbol = OPERATION_SYMBOLS[operation_name]
        print(
            OPERATION_COLORS[operation_name]
            + f"For {operation_name}, enter: {', '.join(aliases[:-1])}, or {symbol}"
        )

    print("----------------------------------------------------------------")
    print("Type 'help' for commands, 'history' for past results, or 'exit' to quit.")

    while True:
        try:
            operation = input("Choose an operation: ").strip()
            command = operation.lower()

            if command in {"quit", "exit", "q"}:
                print("Goodbye!")
                break
            if command == "help":
                _print_help()
                continue
            if command == "history":
                _print_history(history)
                continue

            # LBYL: reject an unknown operation before prompting for numeric input.
            if command not in VALID_OPERATIONS:
                raise ValueError(INVALID_OPERATION_MESSAGE)

            first_number = _parse_number(input("Enter the first number: ").strip(), "first")
            second_number = _parse_number(input("Enter the second number: ").strip(), "second")
            calculation = CalculationFactory.create_calculation(first_number, command, second_number)
            result = calculation.calculate()
            history.append(calculation)
            print(f"Result: {result}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except ValueError as exc:
            print(f"Error: {exc}")
        except ZeroDivisionError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    run_interactive()