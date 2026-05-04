"""Processing strategies and chain composition."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from enum import Enum
from typing import Any

from data_processing.models import DataRecord, JsonObject
from exceptions.custom import InvalidDataError, ProcessingError
from utils.logging import log_call

LOGGER = logging.getLogger(__name__)
DEFAULT_TIMESTAMP = "2024-01-01"


class Operation(str, Enum):
    """Supported single-step processing operations."""

    FILTER = "filter"
    TRANSFORM = "transform"
    VALIDATE = "validate"


class RecordProcessor(ABC):
    """Base class for processors in a Chain of Responsibility."""

    def __init__(self) -> None:
        self._next_processor: RecordProcessor | None = None

    def set_next(self, processor: RecordProcessor) -> RecordProcessor:
        """Attach and return the next processor in the chain."""

        self._next_processor = processor
        return processor

    def handle(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        """Process records and pass them to the next processor if present."""

        processed = self.apply(records)
        if self._next_processor is None:
            return processed
        return self._next_processor.handle(processed)

    @abstractmethod
    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        """Apply this processor to ``records``."""


class ActiveStatusFilter(RecordProcessor):
    """Keep only records whose status is ``active``."""

    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        """Filter inactive records."""

        return [record for record in records if record.is_active]


class TransformProcessor(RecordProcessor):
    """Mark records as processed without mutating the source objects."""

    def __init__(self, timestamp: str = DEFAULT_TIMESTAMP) -> None:
        super().__init__()
        self.timestamp = timestamp

    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        """Add processing metadata to each record."""

        return [record.mark_processed(self.timestamp) for record in records]


class ValidRecordFilter(RecordProcessor):
    """Keep records that satisfy validation rules."""

    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        """Filter invalid records."""

        return [record for record in records if record.is_valid]


class ProcessingChain:
    """Factory-created chain for the standard data-processing workflow."""

    def __init__(self, processors: list[RecordProcessor]) -> None:
        """Create a processing chain.

        Args:
            processors: Ordered processors to apply.

        Raises:
            ValueError: If no processors are supplied.
        """

        if not processors:
            raise ValueError("At least one processor is required")
        self._first = processors[0]
        current = self._first
        for processor in processors[1:]:
            current = current.set_next(processor)

    @classmethod
    def standard(cls, timestamp: str = DEFAULT_TIMESTAMP) -> ProcessingChain:
        """Create the default filter-transform-validate chain."""

        return cls(
            [
                ActiveStatusFilter(),
                TransformProcessor(timestamp=timestamp),
                ValidRecordFilter(),
            ]
        )

    def run(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        """Run records through the configured chain."""

        return self._first.handle(records)


@log_call(LOGGER)
def process_records(
    raw_records: Iterable[Mapping[str, Any]],
    operation: Operation | str,
    *,
    timestamp: str = DEFAULT_TIMESTAMP,
) -> list[JsonObject]:
    """Process JSON-like records with one operation.

    Args:
        raw_records: Iterable of JSON-like mappings.
        operation: Operation enum or matching operation string.
        timestamp: Timestamp used by the transform operation.

    Returns:
        Processed records serialized as dictionaries.

    Raises:
        InvalidDataError: If a record cannot be normalized.
        ProcessingError: If the operation is unknown.
    """

    parsed_operation = _parse_operation(operation)
    records = _to_records(raw_records)
    processor = _processor_for(parsed_operation, timestamp)
    return [record.to_dict() for record in processor.handle(records)]


def _parse_operation(operation: Operation | str) -> Operation:
    """Normalize an operation value."""

    try:
        return operation if isinstance(operation, Operation) else Operation(operation)
    except ValueError as exc:
        raise ProcessingError(f"Unsupported processing operation: {operation}") from exc


def _to_records(raw_records: Iterable[Mapping[str, Any]]) -> list[DataRecord]:
    """Normalize raw mappings to ``DataRecord`` objects."""

    records: list[DataRecord] = []
    for index, raw_record in enumerate(raw_records):
        try:
            records.append(DataRecord.from_mapping(raw_record))
        except TypeError as exc:
            raise InvalidDataError(f"Invalid record at index {index}: {exc}") from exc
    return records


def _processor_for(operation: Operation, timestamp: str) -> RecordProcessor:
    """Create the processor for a single operation."""

    if operation is Operation.FILTER:
        return ActiveStatusFilter()
    if operation is Operation.TRANSFORM:
        return TransformProcessor(timestamp=timestamp)
    return ValidRecordFilter()
