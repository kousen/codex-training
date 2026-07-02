"""Validation decorators for calculator and data-processing operations."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from src.exceptions import DataValidationError

T = TypeVar("T")
R = TypeVar("R")


def validate_numeric_operands(
    func: Callable[[T, float, float], float],
) -> Callable[[T, float, float], float]:
    """Ensure calculator strategies receive numeric operands.

    Args:
        func: Operation method to wrap.

    Returns:
        Wrapped operation method.

    Raises:
        DataValidationError: If either operand is not numeric.
    """

    @wraps(func)
    def wrapper(self: T, left: float, right: float) -> float:
        """Validate operands before calling the wrapped operation."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise DataValidationError("Calculator operands must be numeric")
        return func(self, float(left), float(right))

    return wrapper


def validate_records(
    func: Callable[[T, list[R]], list[R]],
) -> Callable[[T, list[R]], list[R]]:
    """Ensure data processors receive a list of ``Record`` instances.

    Args:
        func: Data processor method to wrap.

    Returns:
        Wrapped processor method.

    Raises:
        DataValidationError: If the input is not a list of ``Record`` objects.
    """

    @wraps(func)
    def wrapper(self: T, records: list[R]) -> list[R]:
        """Validate records before calling the wrapped processor."""
        from src.data_processing.models import Record

        if not isinstance(records, list):
            raise DataValidationError("Records must be provided as a list")
        if not all(isinstance(record, Record) for record in records):
            raise DataValidationError("All records must be Record instances")
        return func(self, records)

    return wrapper
