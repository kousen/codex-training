"""Custom exceptions for the refactored data processor."""

from .custom import (
    CalculatorError,
    DataLoadError,
    DataProcessingError,
    DataSaveError,
    DivisionByZeroError,
    InvalidOperandError,
    InvalidRecordError,
    UnsupportedOperationError,
    UnsupportedProcessTypeError,
)

__all__ = [
    "CalculatorError",
    "DataLoadError",
    "DataProcessingError",
    "DataSaveError",
    "DivisionByZeroError",
    "InvalidRecordError",
    "InvalidOperandError",
    "UnsupportedOperationError",
    "UnsupportedProcessTypeError",
]
