"""Unit tests for processing strategies and chains."""

from __future__ import annotations

import pytest

from data_processing.models import DataRecord
from data_processing.processors import (
    ActiveStatusFilter,
    Operation,
    ProcessingChain,
    TransformProcessor,
    ValidRecordFilter,
    process_records,
)
from exceptions.custom import InvalidDataError, ProcessingError


def test_active_status_filter_keeps_active_records() -> None:
    """Only active records remain after filtering."""

    records = [
        DataRecord(id=1, name="Ada", status="active"),
        DataRecord(id=2, name="Grace", status="inactive"),
    ]

    assert ActiveStatusFilter().handle(records) == [records[0]]


def test_transform_processor_marks_records() -> None:
    """Transform processor adds processing metadata."""

    result = TransformProcessor(timestamp="now").handle(
        [DataRecord(id=1, name="Ada", status="active")]
    )

    assert result == [
        DataRecord(id=1, name="Ada", status="active", processed=True, timestamp="now")
    ]


def test_valid_record_filter_removes_invalid_records() -> None:
    """Validation removes bad ids and blank names."""

    records = [
        DataRecord(id=1, name="Ada", status="active"),
        DataRecord(id=0, name="Zero", status="active"),
        DataRecord(id=2, name="", status="active"),
    ]

    assert ValidRecordFilter().handle(records) == [records[0]]


def test_processing_chain_requires_processors() -> None:
    """An empty chain is invalid configuration."""

    with pytest.raises(ValueError, match="At least one"):
        ProcessingChain([])


def test_standard_chain_filters_transforms_and_validates() -> None:
    """The standard chain applies the complete workflow."""

    records = [
        DataRecord(id=1, name="Ada", status="active"),
        DataRecord(id=2, name="Grace", status="inactive"),
        DataRecord(id=0, name="", status="active"),
    ]

    assert ProcessingChain.standard("today").run(records) == [
        DataRecord(
            id=1,
            name="Ada",
            status="active",
            processed=True,
            timestamp="today",
        )
    ]


@pytest.mark.parametrize(
    ("operation", "expected_ids"),
    [
        (Operation.FILTER, [1, 0]),
        ("filter", [1, 0]),
        ("validate", [1, 2]),
    ],
)
def test_process_records_filters(
    sample_records: list[dict[str, object]],
    operation: Operation | str,
    expected_ids: list[int],
) -> None:
    """Single-operation processing accepts enum and string operations."""

    result = process_records(sample_records, operation)

    assert [record["id"] for record in result] == expected_ids


def test_process_records_transforms_without_mutating_source(
    sample_records: list[dict[str, object]],
) -> None:
    """Transform returns new dictionaries and leaves source data untouched."""

    result = process_records(sample_records[:1], "transform", timestamp="today")

    assert result[0]["processed"] is True
    assert result[0]["timestamp"] == "today"
    assert "processed" not in sample_records[0]


def test_process_records_rejects_unknown_operation(
    sample_records: list[dict[str, object]],
) -> None:
    """Unknown operation names fail loudly."""

    with pytest.raises(ProcessingError, match="Unsupported"):
        process_records(sample_records, "archive")


def test_process_records_rejects_invalid_record() -> None:
    """Invalid record types are wrapped in a domain exception."""

    with pytest.raises(InvalidDataError, match="index 0"):
        process_records([{"id": "bad", "name": "Ada", "status": "active"}], "filter")
