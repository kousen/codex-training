"""Data models used by the processing pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable, Tuple

from exceptions.custom import DataProcessingError
from utils.validators import ensure_non_empty_string, ensure_numeric


@dataclass(slots=True, frozen=True)
class EmployeeRecord:
    """Representation of a single employee row from the dataset."""

    name: str
    age: int
    salary: float

    @classmethod
    def from_csv_row(cls, row: Tuple[str, str, str]) -> "EmployeeRecord":
        """Create an employee record from a CSV row tuple."""
        name_raw, age_raw, salary_raw = row
        name = ensure_non_empty_string(name_raw, name="employee name")
        age = int(ensure_numeric(age_raw, name="employee age"))
        if age < 0:
            raise DataProcessingError("Employee age must be non-negative")
        salary = ensure_numeric(salary_raw, name="employee salary")
        if salary < 0:
            raise DataProcessingError("Employee salary must be non-negative")
        return cls(name=name, age=age, salary=salary)


@dataclass(slots=True, frozen=True)
class SalaryStatistics:
    """Aggregate salary metrics for a collection of employee records."""

    average: float
    minimum: float
    maximum: float

    @classmethod
    def from_records(cls, records: Iterable[EmployeeRecord]) -> "SalaryStatistics":
        """Compute summary statistics from an iterable of employees."""
        salaries = [record.salary for record in records]
        if not salaries:
            raise DataProcessingError("Cannot compute statistics for zero records")
        return cls(average=mean(salaries), minimum=min(salaries), maximum=max(salaries))
