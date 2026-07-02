"""Context-managed JSON record writers."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from types import TracebackType
from typing import Optional, TextIO

from src.data_processing.models import Record
from src.exceptions import DataSaveError

logger = logging.getLogger(__name__)


class JsonRecordWriter:
    """Write records to a JSON file using an explicit context manager."""

    def __init__(self, filename: str) -> None:
        self.path = Path(filename)
        self._file: Optional[TextIO] = None

    def __enter__(self) -> JsonRecordWriter:
        try:
            self._file = self.path.open("w")
            return self
        except OSError as error:
            logger.exception("Unable to open output file: %s", self.path)
            raise DataSaveError(f"Unable to open output file: {self.path}") from error

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._file is not None:
            self._file.close()

    def write(self, records: list[Record]) -> None:
        """Write dataclass records as JSON data."""
        if self._file is None:
            raise DataSaveError("Writer must be opened before writing")
        try:
            json.dump([record.to_dict() for record in records], self._file)
        except OSError as error:
            logger.exception("Unable to save results to %s", self.path)
            raise DataSaveError(f"Unable to save results to {self.path}") from error
