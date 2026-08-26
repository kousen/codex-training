"""Unit tests for processing strategies and pipelines."""

from datetime import datetime, timedelta, timezone
from typing import cast

import pytest

from codex_refactoring.data_processing.models import Record
from codex_refactoring.data_processing.processors import (
    ActiveRecordFilter,
    Operation,
    ProcessingPipeline,
    RecordTransformer,
    RecordValidator,
    build_default_pipeline,
    create_processor,
    process_records,
    utc_now,
)
from codex_refactoring.exceptions import RecordValidationError, UnknownOperationError

FIXED_TIME = datetime(2026, 8, 26, 15, 30, tzinfo=timezone.utc)


def fixed_clock() -> datetime:
    """Return a deterministic processing time."""
    return FIXED_TIME


def test_utc_now_is_timezone_aware() -> None:
    """The production clock returns an aware UTC datetime."""
    current_time = utc_now()
    assert current_time.tzinfo is timezone.utc


def test_filter_keeps_only_active_records_and_returns_copies() -> None:
    """Filtering excludes inactive records without exposing original mappings."""
    active: Record = {"id": 1, "name": "Ada", "status": "active"}
    inactive: Record = {"id": 2, "name": "Grace", "status": "inactive"}

    result = ActiveRecordFilter().process([active, inactive])

    assert result == [active]
    assert result[0] is not active


def test_processors_do_not_share_nested_mutable_values() -> None:
    """Returned records remain isolated even when JSON fields are nested."""
    original: Record = {
        "id": 1,
        "name": "Ada",
        "status": "active",
        "metadata": {"tags": ["pioneer"]},
    }

    filtered = ActiveRecordFilter().process([original])
    transformed = RecordTransformer(fixed_clock).process([original])
    validated = RecordValidator().process([original])
    pipeline_copy = ProcessingPipeline([]).process([original])

    for result in [filtered, transformed, validated, pipeline_copy]:
        assert result[0]["metadata"] == original["metadata"]
        metadata = result[0]["metadata"]
        assert isinstance(metadata, dict)
        tags = metadata["tags"]
        assert isinstance(tags, list)
        tags.append("changed")

    assert original["metadata"] == {"tags": ["pioneer"]}


@pytest.mark.parametrize("status", [None, 1, True])
def test_filter_rejects_missing_or_non_string_status(status: object) -> None:
    """Filtering reports malformed status fields with their record index."""
    record = cast(Record, {"id": 1, "name": "Ada", "status": status})

    with pytest.raises(RecordValidationError, match="index 0.*status") as error:
        ActiveRecordFilter().process([record])

    assert error.value.index == 0
    assert error.value.reason == "'status' must be a string"


def test_transform_adds_one_utc_timestamp_without_mutating_input() -> None:
    """Transformation returns copies and normalizes the clock value to UTC."""
    record: Record = {"id": 1, "name": "Ada"}
    eastern = timezone(timedelta(hours=-4))

    result = RecordTransformer(
        lambda: datetime(2026, 8, 26, 11, 30, tzinfo=eastern)
    ).process([record])

    assert result == [
        {
            "id": 1,
            "name": "Ada",
            "processed": True,
            "timestamp": "2026-08-26T15:30:00Z",
        }
    ]
    assert record == {"id": 1, "name": "Ada"}


def test_transform_empty_input_does_not_read_clock() -> None:
    """An empty transformation avoids unnecessary clock calls."""

    def failing_clock() -> datetime:
        raise AssertionError("clock should not be called")

    assert RecordTransformer(failing_clock).process([]) == []


def test_transform_rejects_naive_clock() -> None:
    """A clock without timezone information cannot create an unambiguous timestamp."""
    transformer = RecordTransformer(lambda: datetime(2026, 8, 26))

    with pytest.raises(ValueError, match="timezone-aware"):
        transformer.process([{"id": 1}])


def test_validator_accepts_valid_records_and_returns_copies() -> None:
    """Validation preserves valid values while isolating returned mappings."""
    record: Record = {"id": 1, "name": " Ada ", "extra": "allowed"}

    result = RecordValidator().process([record])

    assert result == [record]
    assert result[0] is not record


@pytest.mark.parametrize("record_id", [None, True, 0, -1, 1.5, "1"])
def test_validator_rejects_invalid_ids(record_id: object) -> None:
    """IDs must be real positive integers, not booleans or coercible values."""
    record = cast(Record, {"id": record_id, "name": "Ada"})

    with pytest.raises(RecordValidationError, match="positive integer"):
        RecordValidator().process([record])


@pytest.mark.parametrize("name", [None, "", "   ", 42])
def test_validator_rejects_invalid_names(name: object) -> None:
    """Names must contain non-whitespace text."""
    record = cast(Record, {"id": 1, "name": name})

    with pytest.raises(RecordValidationError, match="non-empty string"):
        RecordValidator().process([record])


def test_factory_creates_each_strategy() -> None:
    """The processor factory supports enum and string operation values."""
    assert isinstance(create_processor(Operation.FILTER), ActiveRecordFilter)
    assert isinstance(create_processor("transform", fixed_clock), RecordTransformer)
    assert isinstance(create_processor("validate"), RecordValidator)


def test_factory_rejects_unknown_operation() -> None:
    """Unknown operations fail explicitly and list supported values."""
    with pytest.raises(UnknownOperationError, match="filter, transform, validate"):
        create_processor("archive")


def test_process_records_runs_selected_strategy() -> None:
    """The convenience API delegates to the selected strategy."""
    records: list[Record] = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
    ]
    assert process_records(records, "filter") == [records[0]]


def test_pipeline_chains_processors_in_order() -> None:
    """Each pipeline stage receives the preceding stage's output."""
    records: list[Record] = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
    ]

    result = build_default_pipeline(fixed_clock).process(records)

    assert result == [
        {
            "id": 1,
            "name": "Ada",
            "status": "active",
            "processed": True,
            "timestamp": "2026-08-26T15:30:00Z",
        }
    ]


def test_empty_pipeline_materializes_records() -> None:
    """A pipeline without stages still returns a detached list."""
    record: Record = {"id": 1}
    source = (item for item in [record])

    result = ProcessingPipeline([]).process(source)

    assert result == [record]
