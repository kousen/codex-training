"""Dataclass models for processed records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class Record:
    """Structured representation of a data record."""

    id: Optional[int] = None
    name: str = ""
    status: str = ""
    processed: bool = False
    timestamp: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> Record:
        """Create a record from JSON-style mapping data."""
        raw_id = data.get("id")
        return cls(
            id=raw_id if isinstance(raw_id, int) else None,
            name=str(data.get("name", "")),
            status=str(data.get("status", "")),
            processed=bool(data.get("processed", False)),
            timestamp=str(data["timestamp"]) if "timestamp" in data else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert this record back to JSON-serializable data."""
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
        }
        if self.status:
            data["status"] = self.status
        if self.processed:
            data["processed"] = self.processed
        if self.timestamp is not None:
            data["timestamp"] = self.timestamp
        return data
