"""Project-specific exceptions."""


class DataProcessingError(Exception):
    """Base class for data processing errors."""


class DataLoadError(DataProcessingError):
    """Raised when loading data fails."""


class DataValidationError(DataProcessingError):
    """Raised when data validation fails."""


class DataWriteError(DataProcessingError):
    """Raised when writing data fails."""
