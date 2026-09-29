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
    """Immutable calculation request using a canonical operation name.

    Instances are created by ``CalculationFactory`` and can be retained in the
    current REPL session's history.
    """

    first_number: float
    operation: str
    second_number: float

    def calculate(self) -> float:
        """Execute the stored operation and return its numeric result.

        Raises:
            ZeroDivisionError: If the operation is division and the divisor is zero.
        """
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
        """Normalize an operation alias and construct a calculation instance.

        The operation may be a canonical name, supported alias, or symbol.

        Raises:
            ValueError: If the operation is not supported.
        """
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
    """Evaluate an expression and return its result as a float.

    Raises:
        ValueError: If evaluation fails or the expression returns a non-numeric value.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as exc:
        raise ValueError(f"Invalid expression: {expression}") from exc

    if isinstance(result, (int, float)):
        return float(result)

    raise ValueError(f"Expression did not produce a number: {expression}")