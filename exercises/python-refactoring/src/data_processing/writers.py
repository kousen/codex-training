"""Writers that persist processed data using context managers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from exceptions.custom import FileProcessingError
from utils.validators import ensure_non_empty_string
from .processors import ProcessingPayload


@dataclass(slots=True)
class EmployeeReportWriter:
    """Context manager that writes a textual salary report."""

    path: Path
    _file_handle: TextIO | None = None

    def __enter__(self) -> "EmployeeReportWriter":
        try:
            self._file_handle = self.path.open("w", encoding="utf-8")
        except OSError as exc:  # pragma: no cover - dependent on OS
            raise FileProcessingError(f"Unable to open file for writing: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

    def write(self, payload: ProcessingPayload) -> None:
        if self._file_handle is None:
            raise FileProcessingError("Writer must be used as a context manager")

        statistics = payload.context.get("salary_statistics")
        if statistics is None:
            raise FileProcessingError("Payload does not contain salary statistics")

        lines = [
            "Salary Report",
            "=" * 40,
        ]
        for record in payload.records:
            lines.append(f"{record.name:<20} | Age: {record.age:>2} | Salary: ${record.salary:,.2f}")

        lines.extend(
            [
                "=" * 40,
                f"Average Salary: ${statistics.average:,.2f}",
                f"Minimum Salary: ${statistics.minimum:,.2f}",
                f"Maximum Salary: ${statistics.maximum:,.2f}",
            ]
        )

        self._file_handle.write("\n".join(lines))


def resolve_output_path(path_str: str) -> Path:
    """Validate and convert a string path to a filesystem path."""
    cleaned = ensure_non_empty_string(path_str, name="output path")
    return Path(cleaned).expanduser().resolve()
