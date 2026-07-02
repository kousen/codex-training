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
    """Ensure calculator strategies receive numeric operands."""

    @wraps(func)
    def wrapper(self: T, left: float, right: float) -> float:
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise DataValidationError("Calculator operands must be numeric")
        return func(self, float(left), float(right))

    return wrapper


def validate_records(
    func: Callable[[T, list[R]], list[R]],
) -> Callable[[T, list[R]], list[R]]:
    """Ensure data processors receive a list of ``Record`` instances."""

    @wraps(func)
    def wrapper(self: T, records: list[R]) -> list[R]:
        from src.data_processing.models import Record

        if not isinstance(records, list):
            raise DataValidationError("Records must be provided as a list")
        if not all(isinstance(record, Record) for record in records):
            raise DataValidationError("All records must be Record instances")
        return func(self, records)

    return wrapper
