"""Data models used in the processing pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from exceptions.custom import DataValidationError


@dataclass(slots=True)
class Record:
    """Represents a data item in the processing pipeline."""

    record_id: int
    name: str
    status: str | None = None
    processed: bool = False
    timestamp: str | None = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "Record":
        """Create a Record from a mapping, validating required fields."""
        try:
            record_id = int(mapping["id"])
            name = str(mapping["name"])
        except (KeyError, TypeError, ValueError) as exc:
            raise DataValidationError("Invalid record data") from exc

        status = mapping.get("status")
        processed = bool(mapping.get("processed", False))
        timestamp = mapping.get("timestamp")

        return cls(
            record_id=record_id,
            name=name,
            status=str(status) if status is not None else None,
            processed=processed,
            timestamp=str(timestamp) if timestamp is not None else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the Record back to a serializable dict."""
        data: dict[str, Any] = {
            "id": self.record_id,
            "name": self.name,
            "processed": self.processed,
        }
        if self.status is not None:
            data["status"] = self.status
        if self.timestamp is not None:
            data["timestamp"] = self.timestamp
        return data
