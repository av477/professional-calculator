"""Higher-level calculation behavior."""

from dataclasses import dataclass

from app.operation import (
    INVALID_OPERATION_MESSAGE,
    OPERATIONS,
    OPERATION_SYMBOLS,
    VALID_OPERATIONS,
)


@dataclass(frozen=True)
class Calculation:
    """A calculation request that can be executed and retained in session history."""

    first_number: float
    operation: str
    second_number: float

    def calculate(self) -> float:
        """Execute this calculation and return its result."""
        return OPERATIONS[self.operation](self.first_number, self.second_number)

    @property
    def symbol(self) -> str:
        """Return the arithmetic symbol for this calculation."""
        return OPERATION_SYMBOLS[self.operation]


class CalculationFactory:
    """Create calculation instances from operation names, aliases, or symbols."""

    @staticmethod
    def create_calculation(
        first_number: float,
        operation: str,
        second_number: float,
    ) -> Calculation:
        """Validate an operation and construct its calculation instance."""
        normalized_operation = operation.strip().lower()
        if normalized_operation not in VALID_OPERATIONS:
            raise ValueError(INVALID_OPERATION_MESSAGE)

        canonical_operation = VALID_OPERATIONS[normalized_operation]
        return Calculation(first_number, canonical_operation, second_number)


def calculate(first_number: float, operation: str, second_number: float) -> float:
    """Perform a calculation based on a user-selected operation."""
    calculation = CalculationFactory.create_calculation(first_number, operation, second_number)
    return calculation.calculate()


def evaluate_expression(expression: str) -> float:
    """Evaluate an arithmetic expression using Python's evaluator."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as exc:
        raise ValueError(f"Invalid expression: {expression}") from exc

    if isinstance(result, (int, float)):
        return float(result)

    raise ValueError(f"Expression did not produce a number: {expression}")