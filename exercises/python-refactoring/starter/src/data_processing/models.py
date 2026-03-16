"""Domain models for the data processor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from exceptions.custom import InvalidRecordError


@dataclass(slots=True)
class ProcessingRecord:
    """Normalized representation of an input record.

    Attributes:
        id: Positive identifier when present.
        name: Human-readable record name.
        status: Current workflow status.
        processed: Whether the transform step has run.
        timestamp: ISO-formatted processing timestamp.
        extra_fields: Any additional payload preserved from the source data.
    """

    id: int | None = None
    name: str | None = None
    status: str | None = None
    processed: bool = False
    timestamp: str | None = None
    extra_fields: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, raw_record: dict[str, Any]) -> "ProcessingRecord":
        """Create a record from a JSON-compatible mapping.

        Args:
            raw_record: Untrusted source mapping.

        Returns:
            Normalized record instance.

        Raises:
            InvalidRecordError: If the input is not a dictionary.
        """

        if not isinstance(raw_record, dict):
            raise InvalidRecordError(
                f"Expected each record to be a dictionary, got {type(raw_record)!r}."
            )

        known_fields = {"id", "name", "status", "processed", "timestamp"}
        extra_fields = {
            key: value for key, value in raw_record.items() if key not in known_fields
        }

        return cls(
            id=raw_record.get("id"),
            name=raw_record.get("name"),
            status=raw_record.get("status"),
            processed=bool(raw_record.get("processed", False)),
            timestamp=raw_record.get("timestamp"),
            extra_fields=extra_fields,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the record back into a plain dictionary."""

        payload: dict[str, Any] = dict(self.extra_fields)
        payload.update(
            {
                "id": self.id,
                "name": self.name,
                "status": self.status,
                "processed": self.processed,
                "timestamp": self.timestamp,
            }
        )
        return payload
