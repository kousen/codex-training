"""Unit tests for processing pipeline steps."""

from __future__ import annotations

import pytest

from data_processing.models import Record
from data_processing.processors import (
    FilterProcessor,
    Processor,
    TransformProcessor,
    ValidateProcessor,
    build_default_pipeline,
)


def test_filter_processor_keeps_matching_status() -> None:
    records = [
        Record(record_id=1, name="Ada", status="active"),
        Record(record_id=2, name="Bob", status="inactive"),
    ]

    processor = FilterProcessor(status="active")
    result = processor.handle(records)

    assert [record.record_id for record in result] == [1]


def test_transform_processor_marks_processed() -> None:
    records = [Record(record_id=1, name="Ada", status="active")]

    processor = TransformProcessor(timestamp="2024-02-02")
    result = processor.handle(records)

    assert result[0].processed is True
    assert result[0].timestamp == "2024-02-02"


def test_validate_processor_filters_invalid() -> None:
    records = [
        Record(record_id=1, name="Ada"),
        Record(record_id=0, name="Zero"),
        Record(record_id=2, name=" "),
    ]

    processor = ValidateProcessor()
    result = processor.handle(records)

    assert [record.record_id for record in result] == [1]


def test_default_pipeline_orders_steps() -> None:
    records = [
        Record(record_id=1, name="Ada", status="active"),
        Record(record_id=2, name="Bob", status="inactive"),
    ]

    pipeline = build_default_pipeline()
    result = pipeline.handle(records)

    assert len(result) == 1
    assert result[0].processed is True
    assert result[0].timestamp is not None


def test_base_processor_handle_raises() -> None:
    processor = Processor()
    with pytest.raises(NotImplementedError):
        processor.handle([])
