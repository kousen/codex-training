"""Calculator operations implemented as interchangeable strategies."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from src.exceptions import DivisionByZeroCalculationError
from src.utils.validators import validate_numeric_operands

logger = logging.getLogger(__name__)


class Operation(ABC):
    """Strategy interface for arithmetic operations."""

    @abstractmethod
    def execute(self, left: float, right: float) -> float:
        """Return the result of applying the operation."""


class AddOperation(Operation):
    """Add two numbers."""

    @validate_numeric_operands
    def execute(self, left: float, right: float) -> float:
        """Return ``left + right``."""
        return left + right


class SubtractOperation(Operation):
    """Subtract the right operand from the left operand."""

    @validate_numeric_operands
    def execute(self, left: float, right: float) -> float:
        """Return ``left - right``."""
        return left - right


class MultiplyOperation(Operation):
    """Multiply two numbers."""

    @validate_numeric_operands
    def execute(self, left: float, right: float) -> float:
        """Return ``left * right``."""
        return left * right


class DivideOperation(Operation):
    """Divide the left operand by the right operand."""

    @validate_numeric_operands
    def execute(self, left: float, right: float) -> float:
        """Return ``left / right``."""
        if right == 0:
            logger.error("Cannot divide %s by zero", left)
            raise DivisionByZeroCalculationError("Cannot divide by zero")
        return left / right
