"""Application exception hierarchy for processing and persistence failures."""


class ProcessingError(Exception):
    """Base class for expected application errors."""


class UnknownOperationError(ProcessingError):
    """Raised when a requested processing operation is unsupported."""


class RecordValidationError(ProcessingError):
    """Raised when a record violates an operation's input contract."""

    def __init__(self, index: int, reason: str) -> None:
        """Create an error identifying the invalid record and reason."""
        self.index = index
        self.reason = reason
        super().__init__(f"Record at index {index} is invalid: {reason}")


class DataReadError(ProcessingError):
    """Raised when input data cannot be read or decoded."""


class InvalidDataFormatError(DataReadError):
    """Raised when decoded input does not contain a list of records."""


class DataWriteError(ProcessingError):
    """Raised when results cannot be serialized or written safely."""
