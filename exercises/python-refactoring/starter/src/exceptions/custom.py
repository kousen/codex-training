"""Domain-specific exceptions for data processing."""


class DataProcessingError(Exception):
    """Base exception for data processing failures."""


class UnsupportedProcessTypeError(DataProcessingError):
    """Raised when a processor mode is not recognized."""


class InvalidRecordError(DataProcessingError):
    """Raised when a record cannot be converted into the domain model."""


class DataLoadError(DataProcessingError):
    """Raised when input data cannot be loaded."""


class DataSaveError(DataProcessingError):
    """Raised when processed data cannot be written."""


class CalculatorError(Exception):
    """Base exception for calculator failures."""


class InvalidOperandError(CalculatorError):
    """Raised when an operand is not a valid number."""


class UnsupportedOperationError(CalculatorError):
    """Raised when a calculator operation is not recognized."""


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
