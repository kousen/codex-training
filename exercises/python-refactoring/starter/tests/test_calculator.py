"""Tests for calculator strategy implementations."""

import pytest
from typing import Union

from src.calculator import (
    AddOperation,
    Calculator,
    DivideOperation,
    MultiplyOperation,
    SubtractOperation,
)


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
    operation: Union[
        AddOperation, SubtractOperation, MultiplyOperation, DivideOperation
    ],
    left: float,
    right: float,
    expected: float,
) -> None:
    calculator = Calculator(operation)

    assert calculator.calculate(left, right) == expected


def test_calculator_can_replace_strategy() -> None:
    calculator = Calculator(AddOperation())

    calculator.set_operation(MultiplyOperation())

    assert calculator.calculate(6.0, 7.0) == 42.0


def test_divide_by_zero_raises_error() -> None:
    calculator = Calculator(DivideOperation())

    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calculator.calculate(10.0, 0.0)
