"""Processing pipeline using Chain of Responsibility."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from data_processing.models import Record

logger = logging.getLogger(__name__)

DEFAULT_TIMESTAMP = "2024-01-01"
DEFAULT_STATUS = "active"


@dataclass
class Processor:
    """Base processor in a chain."""

    next_processor: "Processor | None" = None

    def set_next(self, next_processor: "Processor") -> "Processor":
        """Attach the next processor and return it for chaining."""
        self.next_processor = next_processor
        return next_processor

    def handle(self, records: Iterable[Record]) -> list[Record]:
        """Process records and pass to the next processor."""
        processed = self._handle(records)
        if self.next_processor is None:
            return processed
        return self.next_processor.handle(processed)

    def _handle(self, records: Iterable[Record]) -> list[Record]:
        raise NotImplementedError


class FilterProcessor(Processor):
    """Filters records by status."""

    def __init__(self, status: str = DEFAULT_STATUS) -> None:
        super().__init__()
        self.status = status

    def _handle(self, records: Iterable[Record]) -> list[Record]:
        filtered = [record for record in records if record.status == self.status]
        logger.debug("FilterProcessor kept %s records", len(filtered))
        return filtered


class TransformProcessor(Processor):
    """Transforms records by marking them processed and adding timestamps."""

    def __init__(self, timestamp: str = DEFAULT_TIMESTAMP) -> None:
        super().__init__()
        self.timestamp = timestamp

    def _handle(self, records: Iterable[Record]) -> list[Record]:
        transformed: list[Record] = []
        for record in records:
            record.processed = True
            record.timestamp = self.timestamp
            transformed.append(record)
        logger.debug("TransformProcessor updated %s records", len(transformed))
        return transformed


class ValidateProcessor(Processor):
    """Validates records for required constraints."""

    def _handle(self, records: Iterable[Record]) -> list[Record]:
        validated = [
            record for record in records if record.record_id > 0 and record.name.strip()
        ]
        logger.debug("ValidateProcessor kept %s records", len(validated))
        return validated


def build_default_pipeline() -> Processor:
    """Build the default processing chain."""
    filter_step = FilterProcessor()
    transform_step = TransformProcessor()
    validate_step = ValidateProcessor()

    filter_step.set_next(transform_step).set_next(validate_step)
    return filter_step
