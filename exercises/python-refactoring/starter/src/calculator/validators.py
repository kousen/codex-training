"""Validation helpers for calculator inputs."""

from __future__ import annotations

from exceptions.custom import InvalidOperandError

Number = int | float


def validate_operand(value: object, name: str) -> Number:
    """Validate and normalize a calculator operand.

    Args:
        value: Candidate numeric value.
        name: Human-readable parameter name.

    Returns:
        The validated numeric operand.

    Raises:
        InvalidOperandError: If the operand is not a finite calculator number.
    """

    if isinstance(value, bool) or not isinstance(value, int | float):
        raise InvalidOperandError(f"{name} must be an int or float, got {value!r}.")
    return value
