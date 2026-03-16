"""Chain-of-responsibility handlers and factory helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from data_processing.models import ProcessingRecord
from exceptions.custom import UnsupportedProcessTypeError


class ProcessingMode(str, Enum):
    """Supported processing modes."""

    FILTER = "filter"
    TRANSFORM = "transform"
    VALIDATE = "validate"


@dataclass(slots=True)
class RecordHandler(ABC):
    """Base handler for a record-processing chain."""

    next_handler: "RecordHandler | None" = field(default=None, init=False)

    def set_next(self, handler: "RecordHandler") -> "RecordHandler":
        """Link the next handler in the chain."""

        self.next_handler = handler
        return handler

    def handle(self, records: Sequence[ProcessingRecord]) -> list[ProcessingRecord]:
        """Process records and delegate to the next handler when present."""

        processed_records = self._handle(records)
        if self.next_handler is None:
            return processed_records
        return self.next_handler.handle(processed_records)

    @abstractmethod
    def _handle(self, records: Sequence[ProcessingRecord]) -> list[ProcessingRecord]:
        """Perform the handler's work."""


@dataclass(slots=True)
class FilterActiveHandler(RecordHandler):
    """Retain only active records."""

    active_status: str = "active"

    def _handle(self, records: Sequence[ProcessingRecord]) -> list[ProcessingRecord]:
        """Filter records by status."""

        return [record for record in records if record.status == self.active_status]


@dataclass(slots=True)
class TransformHandler(RecordHandler):
    """Mark records as processed and stamp them."""

    timestamp: str = "2024-01-01"

    @classmethod
    def with_current_date(cls) -> "TransformHandler":
        """Build a transformer using the current UTC date."""

        return cls(timestamp=datetime.now(tz=timezone.utc).date().isoformat())

    def _handle(self, records: Sequence[ProcessingRecord]) -> list[ProcessingRecord]:
        """Apply an immutable transformation to records."""

        transformed: list[ProcessingRecord] = []
        for record in records:
            transformed.append(
                ProcessingRecord(
                    id=record.id,
                    name=record.name,
                    status=record.status,
                    processed=True,
                    timestamp=self.timestamp,
                    extra_fields=dict(record.extra_fields),
                )
            )
        return transformed


@dataclass(slots=True)
class ValidateHandler(RecordHandler):
    """Keep only structurally valid records."""

    def _handle(self, records: Sequence[ProcessingRecord]) -> list[ProcessingRecord]:
        """Validate records against required business rules."""

        return [record for record in records if self._is_valid(record)]

    @staticmethod
    def _is_valid(record: ProcessingRecord) -> bool:
        """Return true when a record satisfies basic constraints."""

        return bool(
            record.id is not None
            and record.id > 0
            and record.name is not None
            and record.name.strip()
        )


class ProcessorFactory:
    """Factory for chain handlers."""

    @staticmethod
    def create(mode: ProcessingMode | str) -> RecordHandler:
        """Create a handler for the requested mode.

        Args:
            mode: Enum or string representation of a processing mode.

        Returns:
            A concrete chain handler.

        Raises:
            UnsupportedProcessTypeError: If the mode is unknown.
        """

        normalized_mode = ProcessorFactory._normalize_mode(mode)
        handler_map: dict[ProcessingMode, type[RecordHandler]] = {
            ProcessingMode.FILTER: FilterActiveHandler,
            ProcessingMode.TRANSFORM: TransformHandler,
            ProcessingMode.VALIDATE: ValidateHandler,
        }
        return handler_map[normalized_mode]()

    @staticmethod
    def create_chain(
        modes: Iterable[ProcessingMode | str],
    ) -> RecordHandler | None:
        """Create a linked chain of handlers for pipeline execution."""

        iterator = iter(modes)
        try:
            first_handler = ProcessorFactory.create(next(iterator))
        except StopIteration:
            return None

        current_handler = first_handler
        for mode in iterator:
            current_handler = current_handler.set_next(ProcessorFactory.create(mode))
        return first_handler

    @staticmethod
    def _normalize_mode(mode: ProcessingMode | str) -> ProcessingMode:
        """Normalize string input into a processing mode."""

        if isinstance(mode, ProcessingMode):
            return mode

        try:
            return ProcessingMode(mode.lower())
        except ValueError as error:
            raise UnsupportedProcessTypeError(
                f"Unsupported processing mode: {mode!r}"
            ) from error
