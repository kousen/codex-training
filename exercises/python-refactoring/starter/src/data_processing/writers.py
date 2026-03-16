"""Output writers for data processing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from data_processing.models import ProcessingRecord
from exceptions.custom import DataSaveError


class JsonRecordWriter:
    """Write processing records to a JSON file."""

    def __init__(self, file_path: Path | str) -> None:
        """Initialize the writer with a file path."""

        self._path = Path(file_path)

    def __enter__(self) -> "JsonRecordWriter":
        """Support context manager usage."""

        return self

    def __exit__(self, exc_type: object, exc: object, exc_tb: object) -> None:
        """No-op exit method to keep resource management explicit."""

    @property
    def path(self) -> Path:
        """Return the output path."""

        return self._path

    def write(self, records: list[ProcessingRecord]) -> None:
        """Persist records to disk as formatted JSON."""

        serialized: list[dict[str, Any]] = [record.to_dict() for record in records]
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("w", encoding="utf-8") as handle:
                json.dump(serialized, handle, indent=2)
        except OSError as error:
            raise DataSaveError(f"Unable to write output file: {self._path}") from error
