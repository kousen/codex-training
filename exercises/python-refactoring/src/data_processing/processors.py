"""Data processing pipeline implemented using the Chain of Responsibility pattern."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional

from exceptions.custom import DataProcessingError
from utils.validators import ensure_sequence_min_length
from .models import EmployeeRecord, SalaryStatistics


@dataclass(slots=True)
class ProcessingPayload:
    """Encapsulates data flowing through the processor chain."""

    records: list[EmployeeRecord]
    context: dict[str, Any] = field(default_factory=dict)


class Processor:
    """Abstract chain element."""

    def __init__(self, successor: "Processor | None" = None) -> None:
        self._successor = successor

    def set_successor(self, successor: "Processor") -> "Processor":
        self._successor = successor
        return successor

    def handle(self, payload: ProcessingPayload) -> ProcessingPayload:
        processed = self.process(payload)
        if self._successor:
            return self._successor.handle(processed)
        return processed

    def process(self, payload: ProcessingPayload) -> ProcessingPayload:  # pragma: no cover - abstract contract
        raise NotImplementedError


class AgeFilterProcessor(Processor):
    """Filter employees outside of allowed age range."""

    def __init__(self, minimum: int | None = None, maximum: int | None = None, *, successor: Processor | None = None) -> None:
        super().__init__(successor)
        self.minimum = minimum
        self.maximum = maximum

    def process(self, payload: ProcessingPayload) -> ProcessingPayload:
        filtered = [
            record
            for record in payload.records
            if (self.minimum is None or record.age >= self.minimum)
            and (self.maximum is None or record.age <= self.maximum)
        ]
        if not filtered:
            raise DataProcessingError("No records remain after applying age filters")
        return ProcessingPayload(records=filtered, context=payload.context)


class SalarySortProcessor(Processor):
    """Sort employees by salary using Python's efficient sorting."""

    def __init__(self, *, descending: bool = False, successor: Processor | None = None) -> None:
        super().__init__(successor)
        self.descending = descending

    def process(self, payload: ProcessingPayload) -> ProcessingPayload:
        sorted_records = sorted(payload.records, key=lambda record: record.salary, reverse=self.descending)
        return ProcessingPayload(records=sorted_records, context=payload.context)


class StatisticsProcessor(Processor):
    """Compute aggregate salary statistics and attach them to the context."""

    def process(self, payload: ProcessingPayload) -> ProcessingPayload:
        payload.context["salary_statistics"] = SalaryStatistics.from_records(payload.records)
        return payload


class PersonLookupProcessor(Processor):
    """Store a quick lookup table for person records."""

    def process(self, payload: ProcessingPayload) -> ProcessingPayload:
        payload.context["index_by_name"] = {record.name.lower(): record for record in payload.records}
        return payload


@dataclass(slots=True)
class EmployeeDataPipeline:
    """Orchestrates the processor chain for employee datasets."""

    head: Processor

    def run(self, records: Iterable[EmployeeRecord]) -> ProcessingPayload:
        materialised = list(records)
        ensure_sequence_min_length(materialised, minimum=1, name="employee records")
        payload = ProcessingPayload(records=materialised)
        return self.head.handle(payload)


def build_default_pipeline(minimum_age: int | None = None, maximum_age: int | None = None, *, descending: bool = False) -> EmployeeDataPipeline:
    """Construct the default processing pipeline."""
    statistics = StatisticsProcessor()
    lookup = PersonLookupProcessor(successor=statistics)
    sorter = SalarySortProcessor(descending=descending, successor=lookup)
    age_filter = AgeFilterProcessor(minimum=minimum_age, maximum=maximum_age, successor=sorter)
    return EmployeeDataPipeline(head=age_filter)


def find_employee(payload: ProcessingPayload, name: str) -> Optional[EmployeeRecord]:
    """Locate an employee by name within the pipeline payload."""
    index = payload.context.get("index_by_name", {})
    return index.get(name.lower()) if isinstance(index, dict) else None
