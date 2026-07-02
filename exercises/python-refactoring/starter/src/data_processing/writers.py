"""Context-managed JSON record writers."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from types import TracebackType
from typing import TextIO

from src.data_processing.models import Record
from src.exceptions import DataSaveError

logger = logging.getLogger(__name__)


class JsonRecordWriter:
    """Write records to a JSON file using an explicit context manager.

    Args:
        filename: Path to the JSON file that should receive records.
    """

    def __init__(self, filename: str) -> None:
        """Initialize the writer.

        Args:
            filename: Path to the JSON output file.
        """
        self.path = Path(filename)
        self._file: TextIO | None = None

    def __enter__(self) -> JsonRecordWriter:
        """Open the output file.

        Returns:
            This writer instance.

        Raises:
            DataSaveError: If the file cannot be opened for writing.
        """
        try:
            self._file = self.path.open("w")
            return self
        except OSError as error:
            logger.exception("Unable to open output file: %s", self.path)
            raise DataSaveError(f"Unable to open output file: {self.path}") from error

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the output file when leaving the context manager.

        Args:
            exc_type: Exception type raised inside the context, if any.
            exc_value: Exception instance raised inside the context, if any.
            traceback: Traceback raised inside the context, if any.
        """
        if self._file is not None:
            self._file.close()

    def write(self, records: list[Record]) -> None:
        """Write dataclass records as JSON data.

        Args:
            records: Records to serialize.

        Raises:
            DataSaveError: If the writer is not open or the file cannot be
                written.
        """
        if self._file is None:
            raise DataSaveError("Writer must be opened before writing")
        try:
            json.dump([record.to_dict() for record in records], self._file)
        except OSError as error:
            logger.exception("Unable to save results to %s", self.path)
            raise DataSaveError(f"Unable to save results to {self.path}") from error
