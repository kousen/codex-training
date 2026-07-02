"""Tests for calculator strategy implementations."""

from __future__ import annotations

import math
from collections.abc import Callable

import pytest

from src.calculator import (
    AddOperation,
    Calculator,
    DivideOperation,
    MultiplyOperation,
    Operation,
    SubtractOperation,
)
from src.exceptions import DataValidationError, DivisionByZeroCalculationError


@pytest.mark.parametrize(
    ("operation", "left", "right", "expected"),
    [
        (AddOperation(), 2.0, 3.0, 5.0),
        (SubtractOperation(), 5.0, 3.0, 2.0),
        (MultiplyOperation(), 4.0, 3.0, 12.0),
        (DivideOperation(), 8.0, 2.0, 4.0),
    ],
)
def test_calculator_uses_configured_strategy(
    operation: Operation,
    left: float,
    right: float,
    expected: float,
) -> None:
    calculator = Calculator(operation)

    assert calculator.calculate(left, right) == expected


@pytest.mark.parametrize(
    ("operation_factory", "left", "right", "expected"),
    [
        (AddOperation, -2.5, 0.5, -2.0),
        (SubtractOperation, -2.5, -0.5, -2.0),
        (MultiplyOperation, -3.0, 2.5, -7.5),
        (DivideOperation, -9.0, 3.0, -3.0),
    ],
)
def test_operations_handle_negative_and_decimal_inputs(
    operation_factory: Callable[[], Operation],
    left: float,
    right: float,
    expected: float,
) -> None:
    operation = operation_factory()

    assert math.isclose(operation.execute(left, right), expected)


def test_calculator_can_replace_strategy() -> None:
    calculator = Calculator(AddOperation())

    calculator.set_operation(MultiplyOperation())

    assert calculator.calculate(6.0, 7.0) == 42.0


def test_divide_by_zero_raises_error() -> None:
    calculator = Calculator(DivideOperation())

    with pytest.raises(DivisionByZeroCalculationError, match="Cannot divide by zero"):
        calculator.calculate(10.0, 0.0)


def test_calculator_validation_decorator_rejects_non_numeric_operands() -> None:
    calculator = Calculator(AddOperation())

    with pytest.raises(DataValidationError, match="operands must be numeric"):
        calculator.calculate("1", 2.0)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("1", 2.0),
        (1.0, object()),
        (None, 2.0),
    ],
)
def test_operation_validation_rejects_non_numeric_operands(
    left: object,
    right: object,
) -> None:
    with pytest.raises(DataValidationError, match="operands must be numeric"):
        AddOperation().execute(left, right)  # type: ignore[arg-type]
