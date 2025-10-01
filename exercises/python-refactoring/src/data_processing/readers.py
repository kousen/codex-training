"""File readers implemented with context managers for safe resource handling."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO

from exceptions.custom import FileProcessingError
from utils.validators import ensure_non_empty_string
from .models import EmployeeRecord


@dataclass(slots=True)
class EmployeeCSVReader:
    """Context manager for reading employee data from a CSV file."""

    path: Path
    _file_handle: TextIO | None = None

    def __enter__(self) -> "EmployeeCSVReader":
        try:
            self._file_handle = self.path.open("r", encoding="utf-8")
        except OSError as exc:  # pragma: no cover - dependent on OS errors
            raise FileProcessingError(f"Unable to open file: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

    def records(self) -> Iterable[EmployeeRecord]:
        """Yield employee records from the underlying CSV source."""
        if self._file_handle is None:
            raise FileProcessingError("Reader must be used as a context manager")

        reader = csv.reader(self._file_handle)
        for row in reader:
            if not row:
                continue
            try:
                yield EmployeeRecord.from_csv_row(tuple(row[:3]))
            except FileProcessingError:
                raise
            except Exception as exc:
                raise FileProcessingError(f"Malformed row in {self.path}: {row}") from exc


def resolve_data_path(path_str: str) -> Path:
    """Validate and convert a string path to a Path object."""
    cleaned = ensure_non_empty_string(path_str, name="path")
    return Path(cleaned).expanduser().resolve()
