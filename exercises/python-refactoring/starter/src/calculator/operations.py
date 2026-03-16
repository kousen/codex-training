"""Calculator strategies."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from calculator.validators import Number, validate_operand
from exceptions.custom import DivisionByZeroError, UnsupportedOperationError


class OperationStrategy(Protocol):
    """Protocol implemented by calculator operations."""

    def execute(self, left: Number, right: Number) -> float:
        """Execute a numeric operation."""


class OperationName(str, Enum):
    """Supported calculator operations."""

    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


@dataclass(slots=True)
class AddOperation:
    """Add two operands."""

    def execute(self, left: Number, right: Number) -> float:
        """Return the sum of two operands."""

        return float(validate_operand(left, "left") + validate_operand(right, "right"))


@dataclass(slots=True)
class SubtractOperation:
    """Subtract the right operand from the left operand."""

    def execute(self, left: Number, right: Number) -> float:
        """Return the difference of two operands."""

        return float(validate_operand(left, "left") - validate_operand(right, "right"))


@dataclass(slots=True)
class MultiplyOperation:
    """Multiply two operands."""

    def execute(self, left: Number, right: Number) -> float:
        """Return the product of two operands."""

        return float(validate_operand(left, "left") * validate_operand(right, "right"))


@dataclass(slots=True)
class DivideOperation:
    """Divide the left operand by the right operand."""

    def execute(self, left: Number, right: Number) -> float:
        """Return the quotient of two operands."""

        validated_left = validate_operand(left, "left")
        validated_right = validate_operand(right, "right")
        if validated_right == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return float(validated_left / validated_right)


class StrategyFactory:
    """Factory for calculator strategies."""

    @staticmethod
    def create(operation: OperationName | str) -> OperationStrategy:
        """Create a strategy for the requested operation."""

        normalized_operation = StrategyFactory._normalize_operation(operation)
        strategy_map: dict[OperationName, type[OperationStrategy]] = {
            OperationName.ADD: AddOperation,
            OperationName.SUBTRACT: SubtractOperation,
            OperationName.MULTIPLY: MultiplyOperation,
            OperationName.DIVIDE: DivideOperation,
        }
        return strategy_map[normalized_operation]()

    @staticmethod
    def _normalize_operation(operation: OperationName | str) -> OperationName:
        """Normalize string input into an operation name."""

        if isinstance(operation, OperationName):
            return operation

        try:
            return OperationName(operation.lower())
        except ValueError as error:
            raise UnsupportedOperationError(
                f"Unsupported calculator operation: {operation!r}"
            ) from error
