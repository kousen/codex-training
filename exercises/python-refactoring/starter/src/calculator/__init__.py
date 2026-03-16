"""Calculator package using the Strategy pattern."""

from .calculator import Calculator
from .operations import (
    AddOperation,
    DivideOperation,
    MultiplyOperation,
    OperationName,
    StrategyFactory,
    SubtractOperation,
)

__all__ = [
    "AddOperation",
    "Calculator",
    "DivideOperation",
    "MultiplyOperation",
    "OperationName",
    "StrategyFactory",
    "SubtractOperation",
]
