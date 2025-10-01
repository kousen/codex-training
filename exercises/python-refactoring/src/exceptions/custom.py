"""Custom exception hierarchy for the refactored project."""

from __future__ import annotations


class ProjectError(Exception):
    """Base exception for project-specific errors."""


class CalculatorError(ProjectError):
    """Raised for calculator-related failures."""


class OperationNotSupportedError(CalculatorError):
    """Raised when a requested calculator operation is unavailable."""


class ValidationError(ProjectError):
    """Raised when user-provided input fails validation checks."""


class DataProcessingError(ProjectError):
    """Raised for issues encountered while processing data."""


class FileProcessingError(DataProcessingError):
    """Raised when interaction with external files fails."""


class TemperatureConversionError(ProjectError):
    """Raised when a temperature conversion cannot be performed."""
