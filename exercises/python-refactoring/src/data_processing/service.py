"""High level service encapsulating data processing workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Iterable, List

from exceptions.custom import DataProcessingError
from utils.logging import get_logger
from .models import EmployeeRecord
from .processors import ProcessingPayload, build_default_pipeline, find_employee
from .readers import EmployeeCSVReader, resolve_data_path

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class EmployeeDataService:
    """Service responsible for loading and processing employee data."""

    records: List[EmployeeRecord] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: str | Path) -> "EmployeeDataService":
        resolved = resolve_data_path(str(path))
        with EmployeeCSVReader(resolved) as reader:
            records = list(reader.records())
        if not records:
            raise DataProcessingError(f"No records found in {resolved}")
        LOGGER.info("Loaded %s employee records from %s", len(records), resolved)
        return cls(records=records)

    def average_salary(self) -> float:
        """Compute the average salary for loaded records."""
        return mean(record.salary for record in self.records)

    def find(self, name: str) -> EmployeeRecord | None:
        """Locate a person by name using the processing pipeline's index."""
        payload = self._run_pipeline()
        return find_employee(payload, name)

    def filter_by_age(self, *, minimum: int | None = None, maximum: int | None = None) -> List[EmployeeRecord]:
        """Return employees whose ages fall within the provided bounds."""
        payload = self._run_pipeline(minimum_age=minimum, maximum_age=maximum)
        return payload.records

    def sort_by_salary(self, *, descending: bool = False) -> List[EmployeeRecord]:
        """Return records sorted by salary without mutating internal state."""
        payload = self._run_pipeline(descending=descending)
        return payload.records

    def generate_report_payload(self, *, minimum_age: int | None = None, maximum_age: int | None = None, descending: bool = False) -> ProcessingPayload:
        """Prepare a payload ready for report writing."""
        return self._run_pipeline(minimum_age=minimum_age, maximum_age=maximum_age, descending=descending)

    def _run_pipeline(self, *, minimum_age: int | None = None, maximum_age: int | None = None, descending: bool = False) -> ProcessingPayload:
        pipeline = build_default_pipeline(minimum_age=minimum_age, maximum_age=maximum_age, descending=descending)
        payload = pipeline.run(self.records)
        return payload
