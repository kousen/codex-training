"""Domain models used by the data-processing pipeline."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

JsonValue = str | int | float | bool | None
JsonObject = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class DataRecord:
    """A normalized record from the input JSON document.

    Attributes:
        id: Positive numeric identifier.
        name: Non-empty display name.
        status: Workflow status, such as ``"active"``.
        processed: Whether the transformation stage has processed this record.
        timestamp: Processing timestamp added by the transformation stage.
        extra: Additional scalar fields preserved from the source mapping.
    """

    id: int
    name: str
    status: str
    processed: bool = False
    timestamp: str | None = None
    extra: Mapping[str, JsonValue] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> DataRecord:
        """Create a record from a JSON object.

        Args:
            value: Mapping loaded from JSON.

        Returns:
            A normalized ``DataRecord``.

        Raises:
            TypeError: If required fields have invalid types.
        """

        record_id = value.get("id")
        name = value.get("name")
        status = value.get("status")
        processed = value.get("processed", False)
        timestamp = value.get("timestamp")

        if not isinstance(record_id, int) or isinstance(record_id, bool):
            raise TypeError("record id must be an integer")
        if not isinstance(name, str):
            raise TypeError("record name must be a string")
        if not isinstance(status, str):
            raise TypeError("record status must be a string")
        if not isinstance(processed, bool):
            raise TypeError("record processed flag must be a boolean")
        if timestamp is not None and not isinstance(timestamp, str):
            raise TypeError("record timestamp must be a string when provided")

        known_fields = {"id", "name", "status", "processed", "timestamp"}
        extra = {
            key: item
            for key, item in value.items()
            if key not in known_fields and _is_json_scalar(item)
        }
        return cls(
            id=record_id,
            name=name,
            status=status,
            processed=processed,
            timestamp=timestamp,
            extra=extra,
        )

    @property
    def is_active(self) -> bool:
        """Return whether the record is active."""

        return self.status == "active"

    @property
    def is_valid(self) -> bool:
        """Return whether the record satisfies business validation rules."""

        return self.id > 0 and bool(self.name.strip())

    def mark_processed(self, timestamp: str) -> DataRecord:
        """Return a processed copy of this record.

        Args:
            timestamp: ISO-like timestamp to store on the processed record.

        Returns:
            A new immutable ``DataRecord`` instance.
        """

        return DataRecord(
            id=self.id,
            name=self.name,
            status=self.status,
            processed=True,
            timestamp=timestamp,
            extra=self.extra,
        )

    def to_dict(self) -> JsonObject:
        """Serialize the record to a JSON-compatible dictionary."""

        result: JsonObject = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "processed": self.processed,
        }
        if self.timestamp is not None:
            result["timestamp"] = self.timestamp
        result.update(self.extra)
        return result


def _is_json_scalar(value: object) -> bool:
    """Return whether ``value`` can be safely preserved as a JSON scalar."""

    return value is None or isinstance(value, (str, int, float, bool))
