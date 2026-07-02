"""Calculator that delegates arithmetic to operation strategies."""

from __future__ import annotations

from src.calculator.operations import Operation


class Calculator:
    """Perform calculations using a pluggable operation strategy.

    Args:
        operation: Strategy object that implements the arithmetic operation.
    """

    def __init__(self, operation: Operation) -> None:
        """Initialize the calculator.

        Args:
            operation: Initial operation strategy.
        """
        self.operation = operation

    def set_operation(self, operation: Operation) -> None:
        """Replace the current operation strategy.

        Args:
            operation: New strategy to use for future calculations.
        """
        self.operation = operation

    def calculate(self, left: float, right: float) -> float:
        """Calculate a result using the configured operation.

        Args:
            left: Left operand.
            right: Right operand.

        Returns:
            The result returned by the current operation strategy.

        Raises:
            src.exceptions.CalculationError: If the configured strategy fails.
            src.exceptions.DataValidationError: If operands are not numeric.
        """
        return self.operation.execute(left, right)
