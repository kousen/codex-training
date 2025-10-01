"""Unit tests for the calculator module."""

from __future__ import annotations

import pytest

from calculator.calculator import Calculator
from exceptions.custom import CalculatorError, OperationNotSupportedError


@pytest.mark.parametrize(
    ("operation", "left", "right", "expected"),
    [
        ("add", 1, 2, 3),
        ("sub", 5, 3, 2),
        ("mul", 4, 3, 12),
        ("div", 10, 2, 5),
    ],
)
def test_calculator_operations(operation: str, left: float, right: float, expected: float) -> None:
    calculator = Calculator(log_operations=False)
    assert calculator.calculate(operation, left, right) == pytest.approx(expected)


def test_division_by_zero_raises() -> None:
    calculator = Calculator(log_operations=False)
    with pytest.raises(CalculatorError):
        calculator.calculate("div", 1, 0)


def test_unsupported_operation() -> None:
    calculator = Calculator(log_operations=False)
    with pytest.raises(OperationNotSupportedError):
        calculator.calculate("power", 2, 3)


def test_available_operations() -> None:
    calculator = Calculator(log_operations=False)
    assert set(calculator.available_operations) == {"add", "sub", "mul", "div"}
