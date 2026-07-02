"""Context-managed JSON record readers."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from pathlib import Path
from types import TracebackType
from typing import TextIO

from src.data_processing.models import Record
from src.exceptions import DataLoadError

logger = logging.getLogger(__name__)


class JsonRecordReader:
    """Read records from a JSON file using an explicit context manager.

    Args:
        filename: Path to a JSON file containing a list of record objects.
    """

    def __init__(self, filename: str) -> None:
        """Initialize the reader.

        Args:
            filename: Path to the JSON input file.
        """
        self.path = Path(filename)
        self._file: TextIO | None = None

    def __enter__(self) -> JsonRecordReader:
        """Open the input file.

        Returns:
            This reader instance.

        Raises:
            DataLoadError: If the file cannot be opened.
        """
        try:
            self._file = self.path.open()
            return self
        except FileNotFoundError as error:
            logger.exception("Input file not found: %s", self.path)
            raise DataLoadError(f"Input file not found: {self.path}") from error
        except OSError as error:
            logger.exception("Unable to read input file: %s", self.path)
            raise DataLoadError(f"Unable to read input file: {self.path}") from error

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the input file when leaving the context manager.

        Args:
            exc_type: Exception type raised inside the context, if any.
            exc_value: Exception instance raised inside the context, if any.
            traceback: Traceback raised inside the context, if any.
        """
        if self._file is not None:
            self._file.close()

    def read(self) -> list[Record]:
        """Read JSON data as dataclass records.

        Returns:
            Records parsed from the JSON input file.

        Raises:
            DataLoadError: If the reader is not open, the JSON is invalid, or
                the file does not contain a list of record objects.
        """
        if self._file is None:
            raise DataLoadError("Reader must be opened before reading")
        try:
            raw_data = json.load(self._file)
            if not isinstance(raw_data, list):
                raise TypeError("Expected a list of record objects")
            records: list[Record] = []
            for raw_record in raw_data:
                if not isinstance(raw_record, Mapping):
                    raise TypeError("Expected record objects")
                records.append(Record.from_mapping(raw_record))
            return records
        except json.JSONDecodeError as error:
            logger.exception("Input file contains invalid JSON: %s", self.path)
            raise DataLoadError(f"Invalid JSON in input file: {self.path}") from error
        except (AttributeError, TypeError) as error:
            logger.exception(
                "Input file does not contain record objects: %s", self.path
            )
            raise DataLoadError(
                f"Input file does not contain record objects: {self.path}"
            ) from error
