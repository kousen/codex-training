"""Calculator operations implemented as interchangeable strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Operation(ABC):
    """Strategy interface for arithmetic operations."""

    @abstractmethod
    def execute(self, left: float, right: float) -> float:
        """Return the result of applying the operation."""


class AddOperation(Operation):
    """Add two numbers."""

    def execute(self, left: float, right: float) -> float:
        """Return ``left + right``."""
        return left + right


class SubtractOperation(Operation):
    """Subtract the right operand from the left operand."""

    def execute(self, left: float, right: float) -> float:
        """Return ``left - right``."""
        return left - right


class MultiplyOperation(Operation):
    """Multiply two numbers."""

    def execute(self, left: float, right: float) -> float:
        """Return ``left * right``."""
        return left * right


class DivideOperation(Operation):
    """Divide the left operand by the right operand."""

    def execute(self, left: float, right: float) -> float:
        """Return ``left / right``."""
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return left / right
