"""Tests for domain models."""

from __future__ import annotations

import pytest

from data_processing.models import ProcessingRecord
from exceptions.custom import InvalidRecordError


def test_from_mapping_preserves_known_and_extra_fields() -> None:
    record = ProcessingRecord.from_mapping(
        {
            "id": 7,
            "name": "Delta",
            "status": "active",
            "processed": True,
            "timestamp": "2024-01-01",
            "team": "platform",
        }
    )

    assert record.id == 7
    assert record.name == "Delta"
    assert record.status == "active"
    assert record.processed is True
    assert record.timestamp == "2024-01-01"
    assert record.extra_fields == {"team": "platform"}


def test_from_mapping_rejects_non_dict_inputs() -> None:
    with pytest.raises(InvalidRecordError):
        ProcessingRecord.from_mapping(["not", "a", "mapping"])  # type: ignore[arg-type]


def test_to_dict_round_trips_record() -> None:
    record = ProcessingRecord(
        id=9,
        name="Echo",
        status="active",
        processed=False,
        timestamp=None,
        extra_fields={"priority": "high"},
    )

    assert record.to_dict() == {
        "priority": "high",
        "id": 9,
        "name": "Echo",
        "status": "active",
        "processed": False,
        "timestamp": None,
    }
