"""Tests for the data processing chain."""

from src.data_processing import (
    ActiveRecordFilter,
    ProcessingPipeline,
    Record,
    RequiredFieldsValidator,
    TimestampTransformer,
)


def test_filter_processor_keeps_only_active_records() -> None:
    records: list[Record] = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
    ]

    result = ActiveRecordFilter().process(records)

    assert result == [{"id": 1, "name": "Ada", "status": "active"}]


def test_transform_processor_marks_records_processed() -> None:
    records: list[Record] = [{"id": 1, "name": "Ada"}]

    result = TimestampTransformer(timestamp="2026-07-01").process(records)

    assert result == [
        {
            "id": 1,
            "name": "Ada",
            "processed": True,
            "timestamp": "2026-07-01",
        }
    ]


def test_validator_keeps_records_with_positive_id_and_name() -> None:
    records: list[Record] = [
        {"id": 1, "name": "Ada"},
        {"id": 0, "name": "Grace"},
        {"id": 2, "name": ""},
        {"id": "3", "name": "Katherine"},
    ]

    result = RequiredFieldsValidator().process(records)

    assert result == [{"id": 1, "name": "Ada"}]


def test_pipeline_chains_filter_transform_and_validate() -> None:
    records: list[Record] = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
        {"id": 0, "name": "Barbara", "status": "active"},
        {"id": 3, "name": "", "status": "active"},
    ]
    pipeline = ProcessingPipeline(
        [
            ActiveRecordFilter(),
            TimestampTransformer(),
            RequiredFieldsValidator(),
        ]
    )

    result = pipeline.process(records)

    assert result == [
        {
            "id": 1,
            "name": "Ada",
            "status": "active",
            "processed": True,
            "timestamp": "2024-01-01",
        }
    ]
