"""Dataclass models for processed records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass
class Record:
    """Structured representation of a data record.

    Attributes:
        id: Optional numeric identifier for the record.
        name: Display name used by validation.
        status: Workflow status, such as ``"active"`` or ``"inactive"``.
        processed: Whether the record has passed through the transform step.
        timestamp: Optional timestamp assigned during transformation.
    """

    id: int | None = None
    name: str = ""
    status: str = ""
    processed: bool = False
    timestamp: str | None = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> Record:
        """Create a record from JSON-style mapping data.

        Args:
            data: Mapping loaded from JSON or supplied by legacy callers.

        Returns:
            A normalized ``Record`` dataclass instance.
        """
        raw_id = data.get("id")
        return cls(
            id=raw_id if isinstance(raw_id, int) else None,
            name=str(data.get("name", "")),
            status=str(data.get("status", "")),
            processed=bool(data.get("processed", False)),
            timestamp=str(data["timestamp"]) if "timestamp" in data else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert this record back to JSON-serializable data.

        Returns:
            Dictionary representation suitable for ``json.dump``.
        """
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
