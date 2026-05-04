"""Unit tests for data-processing models."""

from __future__ import annotations

import pytest

from data_processing.models import DataRecord


def test_data_record_from_mapping_preserves_scalar_extra_fields() -> None:
    """Extra scalar fields are retained during normalization."""

    record = DataRecord.from_mapping(
        {
            "id": 1,
            "name": "Ada",
            "status": "active",
            "team": "math",
            "nested": {"ignored": True},
        }
    )

    assert record.extra == {"team": "math"}
    assert record.is_active is True
    assert record.is_valid is True


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"id": "1", "name": "Ada", "status": "active"}, "id"),
        ({"id": True, "name": "Ada", "status": "active"}, "id"),
        ({"id": 1, "name": 42, "status": "active"}, "name"),
        ({"id": 1, "name": "Ada", "status": None}, "status"),
        (
            {"id": 1, "name": "Ada", "status": "active", "processed": "yes"},
            "processed",
        ),
        (
            {"id": 1, "name": "Ada", "status": "active", "timestamp": 100},
            "timestamp",
        ),
    ],
)
def test_data_record_from_mapping_rejects_invalid_types(
    payload: dict[str, object],
    message: str,
) -> None:
    """Normalization rejects invalid required field types."""

    with pytest.raises(TypeError, match=message):
        DataRecord.from_mapping(payload)


def test_data_record_mark_processed_returns_new_instance() -> None:
    """Transformation is immutable."""

    record = DataRecord(id=1, name="Ada", status="active")
    processed = record.mark_processed("2026-05-04")

    assert record.processed is False
    assert processed.processed is True
    assert processed.timestamp == "2026-05-04"
    assert processed.to_dict() == {
        "id": 1,
        "name": "Ada",
        "status": "active",
        "processed": True,
        "timestamp": "2026-05-04",
    }


def test_data_record_validates_trimmed_name() -> None:
    """Whitespace-only names are invalid."""

    assert DataRecord(id=1, name="  ", status="active").is_valid is False
