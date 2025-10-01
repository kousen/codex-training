"""High level calculator interface leveraging operation strategies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from exceptions.custom import CalculatorError, ValidationError
from utils.logging import get_logger
from .operations import LoggingOperation, OperationFactory, Operation, ValidatedOperation

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class Calculator:
    """Orchestrates calculator operations using the Strategy and Decorator patterns."""

    log_operations: bool = True
    _available_operations: List[str] = field(
        default_factory=lambda: list(OperationFactory.available())
    )

    def calculate(self, operation_name: str, left: float, right: float) -> float:
        """Compute a result for the given operation.

        Args:
            operation_name: The symbolic name of the operation to execute.
            left: Left operand.
            right: Right operand.

        Returns:
            The computed floating point result.

        Raises:
            CalculatorError: If the operation is undefined or fails to compute.
        """
        try:
            operation: Operation = OperationFactory.create(operation_name)
            operation = ValidatedOperation(operation)
            if self.log_operations:
                operation = LoggingOperation(operation)
            return operation.compute(left, right)
        except (CalculatorError, ValidationError):
            raise
        except Exception as exc:  # pragma: no cover - defensive guard
            raise CalculatorError("Unexpected calculator failure") from exc

    @property
    def available_operations(self) -> Iterable[str]:
        """List supported operation names."""
        return tuple(self._available_operations)


__all__ = ["Calculator"]
