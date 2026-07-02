"""Data processors implemented with Chain of Responsibility."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Literal, Optional

Record = dict[str, Any]
ProcessType = Literal["filter", "transform", "validate"]


class DataProcessor(ABC):
    """Base handler for a linked data-processing pipeline."""

    def __init__(self) -> None:
        self._next_processor: Optional[DataProcessor] = None

    def set_next(self, processor: DataProcessor) -> DataProcessor:
        """Attach and return the next processor in the chain."""
        self._next_processor = processor
        return processor

    def process(self, records: list[Record]) -> list[Record]:
        """Handle this step, then pass records to the next processor."""
        processed_records = self._handle(records)
        if self._next_processor is None:
            return processed_records
        return self._next_processor.process(processed_records)

    @abstractmethod
    def _handle(self, records: list[Record]) -> list[Record]:
        """Process this pipeline step."""


class ActiveRecordFilter(DataProcessor):
    """Keep only records whose status is active."""

    def _handle(self, records: list[Record]) -> list[Record]:
        return [record for record in records if record.get("status") == "active"]


class TimestampTransformer(DataProcessor):
    """Mark records as processed and add a timestamp."""

    def __init__(self, timestamp: str = "2024-01-01") -> None:
        super().__init__()
        self.timestamp = timestamp

    def _handle(self, records: list[Record]) -> list[Record]:
        transformed_records: list[Record] = []
        for record in records:
            record["processed"] = True
            record["timestamp"] = self.timestamp
            transformed_records.append(record)
        return transformed_records


class RequiredFieldsValidator(DataProcessor):
    """Keep records with a positive id and a non-empty name."""

    def _handle(self, records: list[Record]) -> list[Record]:
        valid_records: list[Record] = []
        for record in records:
            record_id = record.get("id")
            name = record.get("name")
            if isinstance(record_id, int) and record_id > 0 and isinstance(name, str):
                if name:
                    valid_records.append(record)
        return valid_records


class ProcessingPipeline:
    """Convenience wrapper for running one or more processors."""

    def __init__(self, processors: Iterable[DataProcessor]) -> None:
        self.processors = list(processors)

    def process(self, records: list[Record]) -> list[Record]:
        """Run records through the configured processor chain."""
        if not self.processors:
            return records

        for current, next_processor in zip(self.processors, self.processors[1:]):
            current.set_next(next_processor)

        return self.processors[0].process(records)


def processor_for(process_type: ProcessType) -> DataProcessor:
    """Create a processor for a legacy process type."""
    processors: dict[ProcessType, DataProcessor] = {
        "filter": ActiveRecordFilter(),
        "transform": TimestampTransformer(),
        "validate": RequiredFieldsValidator(),
    }
    return processors[process_type]


def build_default_pipeline() -> ProcessingPipeline:
    """Create the default filter-transform-validate processing chain."""
    return ProcessingPipeline(
        [
            ActiveRecordFilter(),
            TimestampTransformer(),
            RequiredFieldsValidator(),
        ]
    )
