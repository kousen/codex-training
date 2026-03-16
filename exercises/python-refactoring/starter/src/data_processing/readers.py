"""Input readers for data processing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from data_processing.models import ProcessingRecord
from exceptions.custom import DataLoadError, InvalidRecordError


class JsonRecordReader:
    """Read processing records from a JSON file."""

    def __init__(self, file_path: Path | str) -> None:
        """Initialize the reader with a file path."""

        self._path = Path(file_path)

    def __enter__(self) -> "JsonRecordReader":
        """Support context manager usage."""

        return self

    def __exit__(self, exc_type: object, exc: object, exc_tb: object) -> None:
        """No-op exit method to keep resource management explicit."""

    @property
    def path(self) -> Path:
        """Return the input path."""

        return self._path

    def read(self) -> list[ProcessingRecord]:
        """Load records from disk.

        Raises:
            DataLoadError: If the file cannot be parsed or validated.
        """

        try:
            with self._path.open("r", encoding="utf-8") as handle:
                payload: Any = json.load(handle)
        except FileNotFoundError as error:
            raise DataLoadError(f"Input file not found: {self._path}") from error
        except json.JSONDecodeError as error:
            raise DataLoadError(f"Invalid JSON in input file: {self._path}") from error
        except OSError as error:
            raise DataLoadError(f"Unable to read input file: {self._path}") from error

        if not isinstance(payload, list):
            raise DataLoadError("Input JSON must contain a list of records.")

        try:
            return [ProcessingRecord.from_mapping(record) for record in payload]
        except InvalidRecordError as error:
            raise DataLoadError("Input JSON contains an invalid record.") from error
