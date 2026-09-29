"""Primitive arithmetic operations used by the calculator."""

OPERATION_ALIASES = {
    "add": ("add", "sum", "+"),
    "subtract": ("subtract", "minus", "-"),
    "multiply": ("multiply", "times", "*"),
    "divide": ("divide", "div", "/"),
}
OPERATION_SYMBOLS = {name: aliases[-1] for name, aliases in OPERATION_ALIASES.items()}
VALID_OPERATIONS = {
    alias: name
    for name, aliases in OPERATION_ALIASES.items()
    for alias in aliases
}
INVALID_OPERATION_MESSAGE = (
    "Invalid operation. Please choose one of: add (+), subtract (-), multiply (*), or divide (/)."
)


def add(first_number: float, second_number: float) -> float:
    """Return the sum of two numbers."""
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    """Return the difference of two numbers."""
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    """Return the product of two numbers."""
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    """Return the quotient of two numbers."""
    if second_number == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return first_number / second_number


OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}