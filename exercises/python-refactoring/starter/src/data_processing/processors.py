"""Data processors implemented with Chain of Responsibility."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from typing import Any, Literal

from src.data_processing.models import Record
from src.exceptions import DataProcessingError, UnsupportedProcessTypeError
from src.utils.validators import validate_records

logger = logging.getLogger(__name__)

RecordInput = Record | Mapping[str, Any]
ProcessType = Literal["filter", "transform", "validate"]


class DataProcessor(ABC):
    """Base handler for a linked data-processing pipeline."""

    def __init__(self) -> None:
        """Initialize a processor without a downstream handler."""
        self._next_processor: DataProcessor | None = None

    def set_next(self, processor: DataProcessor) -> DataProcessor:
        """Attach and return the next processor in the chain.

        Args:
            processor: Processor that should run after this one.

        Returns:
            The same processor, enabling fluent chain construction.
        """
        self._next_processor = processor
        return processor

    @validate_records
    def process(self, records: list[Record]) -> list[Record]:
        """Handle this step, then pass records to the next processor.

        Args:
            records: Dataclass records to process.

        Returns:
            Records after this processor and any downstream processors run.

        Raises:
            DataProcessingError: If this processor cannot handle the records.
        """
        try:
            processed_records = self._handle(records)
            if self._next_processor is None:
                return processed_records
            return self._next_processor.process(processed_records)
        except DataProcessingError:
            raise
        except (KeyError, TypeError, ValueError) as error:
            logger.exception("Processor %s failed", self.__class__.__name__)
            raise DataProcessingError(
                f"{self.__class__.__name__} failed to process records"
            ) from error

    @abstractmethod
    def _handle(self, records: list[Record]) -> list[Record]:
        """Process this pipeline step.

        Args:
            records: Records received by this chain handler.

        Returns:
            Records produced by this handler.
        """


class ActiveRecordFilter(DataProcessor):
    """Keep only records whose status is active."""

    def _handle(self, records: list[Record]) -> list[Record]:
        """Filter records to active records.

        Args:
            records: Records to inspect.

        Returns:
            Records whose ``status`` is ``"active"``.
        """
        return [record for record in records if record.status == "active"]


class TimestampTransformer(DataProcessor):
    """Mark records as processed and add a timestamp.

    Args:
        timestamp: Timestamp value to assign to each transformed record.
    """

    def __init__(self, timestamp: str = "2024-01-01") -> None:
        """Initialize the transformer.

        Args:
            timestamp: Timestamp value to assign to transformed records.
        """
        super().__init__()
        self.timestamp = timestamp

    def _handle(self, records: list[Record]) -> list[Record]:
        """Mark every record as processed.

        Args:
            records: Records to mutate.

        Returns:
            The same records with ``processed`` and ``timestamp`` populated.
        """
        transformed_records: list[Record] = []
        for record in records:
            record.processed = True
            record.timestamp = self.timestamp
            transformed_records.append(record)
        return transformed_records


class RequiredFieldsValidator(DataProcessor):
    """Keep records with a positive id and a non-empty name."""

    def _handle(self, records: list[Record]) -> list[Record]:
        """Filter records to those with required fields.

        Args:
            records: Records to validate.

        Returns:
            Records with a positive ``id`` and non-empty ``name``.
        """
        valid_records: list[Record] = []
        for record in records:
            if record.id is not None and record.id > 0 and record.name:
                valid_records.append(record)
        return valid_records


class ProcessingPipeline:
    """Convenience wrapper for running one or more processors.

    Args:
        processors: Processors to link and run in order.
    """

    def __init__(self, processors: Iterable[DataProcessor]) -> None:
        """Initialize the pipeline.

        Args:
            processors: Processors to link in order.
        """
        self.processors = list(processors)

    def process(self, records: list[Record]) -> list[Record]:
        """Run records through the configured processor chain.

        Args:
            records: Records to process.

        Returns:
            Processed records, or the original list if no processors exist.
        """
        if not self.processors:
            return records

        for current, next_processor in zip(
            self.processors, self.processors[1:], strict=False
        ):
            current.set_next(next_processor)

        return self.processors[0].process(records)


def processor_for(process_type: ProcessType) -> DataProcessor:
    """Create a processor for a legacy process type.

    Args:
        process_type: Legacy operation name: ``"filter"``, ``"transform"``,
            or ``"validate"``.

    Returns:
        A processor matching the requested operation.

    Raises:
        UnsupportedProcessTypeError: If ``process_type`` is unknown.
    """
    processors: dict[ProcessType, DataProcessor] = {
        "filter": ActiveRecordFilter(),
        "transform": TimestampTransformer(),
        "validate": RequiredFieldsValidator(),
    }
    processor = processors.get(process_type)
    if processor is None:
        logger.error("Unsupported process type requested: %s", process_type)
        raise UnsupportedProcessTypeError(f"Unsupported process type: {process_type!r}")
    return processor


def normalize_records(records: Iterable[RecordInput]) -> list[Record]:
    """Convert record inputs into dataclass records.

    Args:
        records: Existing ``Record`` objects or JSON-style mappings.

    Returns:
        Normalized list of ``Record`` instances.
    """
    normalized_records: list[Record] = []
    for record in records:
        if isinstance(record, Record):
            normalized_records.append(record)
        else:
            normalized_records.append(Record.from_mapping(record))
    return normalized_records


def build_default_pipeline() -> ProcessingPipeline:
    """Create the default filter-transform-validate processing chain.

    Returns:
        Pipeline that filters active records, adds processing metadata, and
        validates required fields.
    """
    return ProcessingPipeline(
        [
            ActiveRecordFilter(),
            TimestampTransformer(),
            RequiredFieldsValidator(),
        ]
    )
