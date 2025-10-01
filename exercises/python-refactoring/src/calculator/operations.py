"""Calculator operations implemented using the Strategy pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Protocol

from exceptions.custom import CalculatorError, OperationNotSupportedError
from utils.logging import get_logger
from utils.validators import ensure_numeric

LOGGER = get_logger(__name__)


class Operation(Protocol):
    """Protocol for calculator operations."""

    name: str

    def compute(self, left: float, right: float) -> float:
        """Execute the operation using the provided operands."""


@dataclass(slots=True)
class _BaseOperation(ABC):
    """Abstract base class for all calculator operations."""

    name: str

    @abstractmethod
    def compute(self, left: float, right: float) -> float:
        """Execute the underlying operation."""


@dataclass(slots=True)
class AddOperation(_BaseOperation):
    """Addition strategy."""

    name: str = "add"

    def compute(self, left: float, right: float) -> float:
        return left + right


@dataclass(slots=True)
class SubtractOperation(_BaseOperation):
    """Subtraction strategy."""

    name: str = "sub"

    def compute(self, left: float, right: float) -> float:
        return left - right


@dataclass(slots=True)
class MultiplyOperation(_BaseOperation):
    """Multiplication strategy."""

    name: str = "mul"

    def compute(self, left: float, right: float) -> float:
        return left * right


@dataclass(slots=True)
class DivideOperation(_BaseOperation):
    """Division strategy with zero-division protection."""

    name: str = "div"

    def compute(self, left: float, right: float) -> float:
        if right == 0:
            raise CalculatorError("Division by zero is undefined")
        return left / right


class OperationDecorator(_BaseOperation):
    """Base class for decorators wrapping an operation strategy."""

    def __init__(self, operation: Operation):
        super().__init__(name=operation.name)
        self._operation = operation

    def compute(self, left: float, right: float) -> float:  # pragma: no cover - abstract proxy
        return self._operation.compute(left, right)


class LoggingOperation(OperationDecorator):
    """Decorator that logs operation inputs and outputs."""

    def compute(self, left: float, right: float) -> float:
        LOGGER.info("Executing %s with operands %s and %s", self.name, left, right)
        result = self._operation.compute(left, right)
        LOGGER.info("Result of %s: %s", self.name, result)
        return result


class ValidatedOperation(OperationDecorator):
    """Decorator that validates operands before performing an operation."""

    def compute(self, left: float, right: float) -> float:
        validated_left = ensure_numeric(left, name="left operand")
        validated_right = ensure_numeric(right, name="right operand")
        return self._operation.compute(validated_left, validated_right)


class OperationFactory:
    """Factory responsible for creating calculator operations."""

    _FACTORY: Dict[str, Callable[[], Operation]] = {
        "add": AddOperation,
        "sub": SubtractOperation,
        "mul": MultiplyOperation,
        "div": DivideOperation,
    }

    @classmethod
    def create(cls, name: str) -> Operation:
        """Create an operation strategy by name."""
        try:
            operation = cls._FACTORY[name.lower()]()
        except KeyError as exc:
            raise OperationNotSupportedError(f"Unsupported operation: {name}") from exc
        return operation

    @classmethod
    def available(cls) -> Iterable[str]:
        """Return the supported operation names."""
        return tuple(sorted(cls._FACTORY))


__all__ = [
    "Operation",
    "AddOperation",
    "SubtractOperation",
    "MultiplyOperation",
    "DivideOperation",
    "LoggingOperation",
    "ValidatedOperation",
    "OperationFactory",
]
