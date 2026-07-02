"""Calculator package using the Strategy pattern."""

from src.calculator.calculator import Calculator
from src.calculator.operations import (
    AddOperation,
    DivideOperation,
    MultiplyOperation,
    Operation,
    SubtractOperation,
)

__all__ = [
    "AddOperation",
    "Calculator",
    "DivideOperation",
    "MultiplyOperation",
    "Operation",
    "SubtractOperation",
]
