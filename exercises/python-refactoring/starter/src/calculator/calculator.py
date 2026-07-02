"""Calculator that delegates arithmetic to operation strategies."""

from __future__ import annotations

from src.calculator.operations import Operation


class Calculator:
    """Perform calculations using a pluggable operation strategy."""

    def __init__(self, operation: Operation) -> None:
        self.operation = operation

    def set_operation(self, operation: Operation) -> None:
        """Replace the current operation strategy."""
        self.operation = operation

    def calculate(self, left: float, right: float) -> float:
        """Calculate a result using the configured operation."""
        return self.operation.execute(left, right)
