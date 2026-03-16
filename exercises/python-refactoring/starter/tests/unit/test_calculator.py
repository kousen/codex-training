"""Tests for the calculator strategy implementation."""

from __future__ import annotations

import pytest

from calculator.calculator import Calculator
from calculator.operations import (
    AddOperation,
    DivideOperation,
    MultiplyOperation,
    OperationName,
    StrategyFactory,
    SubtractOperation,
)
from exceptions.custom import (
    DivisionByZeroError,
    InvalidOperandError,
    UnsupportedOperationError,
)


@pytest.mark.parametrize(
    ("operation", "expected_type"),
    [
        (OperationName.ADD, AddOperation),
        ("subtract", SubtractOperation),
        ("multiply", MultiplyOperation),
        ("divide", DivideOperation),
    ],
)
def test_strategy_factory_creates_expected_operation(
    operation: OperationName | str,
    expected_type: type[object],
) -> None:
    assert isinstance(StrategyFactory.create(operation), expected_type)


def test_strategy_factory_rejects_unknown_operation() -> None:
    with pytest.raises(UnsupportedOperationError):
        StrategyFactory.create("power")


@pytest.mark.parametrize(
    ("operation", "left", "right", "expected"),
    [
        ("add", 4, 3, 7.0),
        ("subtract", 4, 3, 1.0),
        ("multiply", 4, 3, 12.0),
        ("divide", 9, 3, 3.0),
    ],
)
def test_calculator_executes_operation(
    operation: str, left: int, right: int, expected: float
) -> None:
    calculator = Calculator()

    assert calculator.calculate(operation, left, right) == expected


def test_calculator_rejects_division_by_zero() -> None:
    calculator = Calculator()

    with pytest.raises(DivisionByZeroError):
        calculator.calculate("divide", 1, 0)


@pytest.mark.parametrize("value", [True, "4", None])
def test_calculator_rejects_invalid_operands(value: object) -> None:
    calculator = Calculator()

    with pytest.raises(InvalidOperandError):
        calculator.calculate("add", value, 2)  # type: ignore[arg-type]
