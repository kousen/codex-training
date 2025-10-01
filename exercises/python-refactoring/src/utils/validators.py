"""Common validation helpers used across the project."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from exceptions.custom import ValidationError

T = TypeVar("T")


def ensure_numeric(value: Any, *, allow_infinite: bool = False, name: str = "value") -> float:
    """Ensure a value can be coerced to a finite floating point number."""
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{name} must be numeric") from exc

    if not allow_infinite and (number == float("inf") or number == float("-inf")):
        raise ValidationError(f"{name} must be finite")

    if number != number:  # NaN check
        raise ValidationError(f"{name} must not be NaN")

    return number


def ensure_non_empty_string(value: Any, *, name: str = "value") -> str:
    """Ensure the provided value is a non-empty string."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")
    return value.strip()


def ensure_sequence_min_length(sequence: Sequence[T] | Iterable[T], *, minimum: int, name: str = "sequence") -> None:
    """Ensure a sequence-like object meets a required minimum length."""
    if minimum < 0:
        raise ValidationError("minimum must be non-negative")

    if isinstance(sequence, Sequence):
        length = len(sequence)
    else:
        length = sum(1 for _ in sequence)

    if length < minimum:
        raise ValidationError(f"{name} must contain at least {minimum} items")
