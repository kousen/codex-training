"""Validators specific to the calculator domain."""

from __future__ import annotations

from exceptions.custom import OperationNotSupportedError
from .operations import OperationFactory


def validate_operation_name(name: str) -> str:
    """Validate and normalise an operation name."""
    canonical = name.lower()
    if canonical not in OperationFactory.available():
        raise OperationNotSupportedError(f"Unsupported operation: {name}")
    return canonical
