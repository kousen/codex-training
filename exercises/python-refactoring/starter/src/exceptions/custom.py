"""Application-specific exceptions for clear failure modes."""


class RefactoringExerciseError(Exception):
    """Base exception for the refactoring exercise."""


class CalculationError(RefactoringExerciseError):
    """Raised when a calculator operation fails."""


class DivisionByZeroCalculationError(CalculationError):
    """Raised when division by zero is requested."""


class DataProcessingError(RefactoringExerciseError):
    """Raised when data processing cannot continue."""


class DataValidationError(DataProcessingError):
    """Raised when input data fails validation."""


class UnsupportedProcessTypeError(DataProcessingError):
    """Raised when a requested processing step is unknown."""


class DataLoadError(DataProcessingError):
    """Raised when input data cannot be loaded."""


class DataSaveError(DataProcessingError):
    """Raised when processed data cannot be saved."""
