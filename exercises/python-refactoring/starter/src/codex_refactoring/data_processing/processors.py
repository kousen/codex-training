"""Composable strategies for filtering, transforming, and validating records."""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable, Sequence
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol

from codex_refactoring.data_processing.models import Record, clone_record
from codex_refactoring.exceptions import RecordValidationError, UnknownOperationError

LOGGER = logging.getLogger(__name__)
Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """Return the current timezone-aware UTC time."""
    return datetime.now(timezone.utc)


class Operation(str, Enum):
    """Supported record-processing operations."""

    FILTER = "filter"
    TRANSFORM = "transform"
    VALIDATE = "validate"


class RecordProcessor(Protocol):
    """Strategy interface implemented by each processing operation."""

    def process(self, records: Iterable[Record]) -> list[Record]:
        """Process records and return a materialized result."""


class ActiveRecordFilter:
    """Keep records whose status is exactly ``active``."""

    def process(self, records: Iterable[Record]) -> list[Record]:
        """Return active records after validating the status field."""
        active_records: list[Record] = []
        for index, record in enumerate(records):
            status = record.get("status")
            if not isinstance(status, str):
                raise RecordValidationError(index, "'status' must be a string")
            if status == "active":
                active_records.append(clone_record(record))
        return active_records


class RecordTransformer:
    """Add processing metadata without mutating caller-owned records."""

    def __init__(self, clock: Clock = utc_now) -> None:
        """Create a transformer with an injectable timestamp source."""
        self._clock = clock

    def process(self, records: Iterable[Record]) -> list[Record]:
        """Return copies marked as processed at one consistent UTC timestamp."""
        materialized_records = list(records)
        if not materialized_records:
            return []

        processing_time = self._clock()
        if processing_time.tzinfo is None or processing_time.utcoffset() is None:
            raise ValueError(
                "The processing clock must return a timezone-aware datetime"
            )
        timestamp = (
            processing_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        transformed_records: list[Record] = []
        for record in materialized_records:
            transformed = clone_record(record)
            transformed["processed"] = True
            transformed["timestamp"] = timestamp
            transformed_records.append(transformed)
        return transformed_records


class RecordValidator:
    """Validate the required identity fields on each record."""

    def process(self, records: Iterable[Record]) -> list[Record]:
        """Return validated record copies or fail fast with a detailed error."""
        validated_records: list[Record] = []
        for index, record in enumerate(records):
            record_id = record.get("id")
            name = record.get("name")

            if type(record_id) is not int or record_id <= 0:
                raise RecordValidationError(index, "'id' must be a positive integer")
            if not isinstance(name, str) or not name.strip():
                raise RecordValidationError(index, "'name' must be a non-empty string")
            validated_records.append(clone_record(record))
        return validated_records


class ProcessingPipeline:
    """Run a sequence of processors as a Chain of Responsibility."""

    def __init__(self, processors: Sequence[RecordProcessor]) -> None:
        """Create a pipeline from processors in execution order."""
        self._processors = tuple(processors)

    def process(self, records: Iterable[Record]) -> list[Record]:
        """Pass each processor's result to the next processor."""
        result = [clone_record(record) for record in records]
        for processor in self._processors:
            LOGGER.debug("Running processor %s", type(processor).__name__)
            result = processor.process(result)
        return result


def create_processor(
    operation: Operation | str, clock: Clock = utc_now
) -> RecordProcessor:
    """Create the strategy for an operation.

    Args:
        operation: An operation enum or its string value.
        clock: Timestamp source used by transformation.

    Raises:
        UnknownOperationError: If the operation is not supported.
    """
    try:
        parsed_operation = Operation(operation)
    except ValueError as exc:
        supported = ", ".join(item.value for item in Operation)
        raise UnknownOperationError(
            f"Unsupported operation {operation!r}; expected one of: {supported}"
        ) from exc

    if parsed_operation is Operation.FILTER:
        return ActiveRecordFilter()
    if parsed_operation is Operation.TRANSFORM:
        return RecordTransformer(clock)
    return RecordValidator()


def process_records(
    records: Iterable[Record],
    operation: Operation | str,
    *,
    clock: Clock = utc_now,
) -> list[Record]:
    """Process records with one selected strategy."""
    return create_processor(operation, clock).process(records)


def build_default_pipeline(clock: Clock = utc_now) -> ProcessingPipeline:
    """Build the default filter, transform, and validate pipeline."""
    return ProcessingPipeline(
        [
            ActiveRecordFilter(),
            RecordTransformer(clock),
            RecordValidator(),
        ]
    )
