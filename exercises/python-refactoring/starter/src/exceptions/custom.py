"""Exception hierarchy for data processing failures."""


class DataProcessingError(Exception):
    """Base class for data-processing errors."""


class ReaderError(DataProcessingError):
    """Raised when input data cannot be read or parsed."""


class WriterError(DataProcessingError):
    """Raised when output data cannot be written."""


class InvalidDataError(DataProcessingError):
    """Raised when input JSON does not match the expected shape."""


class ProcessingError(DataProcessingError):
    """Raised when a processing operation cannot be applied."""
