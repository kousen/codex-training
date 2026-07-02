"""Tests for the data processing chain."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.data_processing import (
    ActiveRecordFilter,
    DataProcessor,
    JsonRecordReader,
    JsonRecordWriter,
    ProcessingPipeline,
    Record,
    RequiredFieldsValidator,
    TimestampTransformer,
    readers,
    writers,
)
from src.data_processing.processors import ProcessType, processor_for
from src.exceptions import (
    DataLoadError,
    DataProcessingError,
    DataSaveError,
    DataValidationError,
    UnsupportedProcessTypeError,
)

PROCESSOR_CASES: list[tuple[ProcessType, type[DataProcessor]]] = [
    ("filter", ActiveRecordFilter),
    ("transform", TimestampTransformer),
    ("validate", RequiredFieldsValidator),
]


def test_filter_processor_keeps_only_active_records(records: list[Record]) -> None:
    result = ActiveRecordFilter().process(records)

    assert result == [
        Record(id=1, name="Ada", status="active"),
        Record(id=0, name="Barbara", status="active"),
        Record(id=3, name="", status="active"),
    ]


def test_transform_processor_marks_records_processed(
    active_valid_record: Record,
) -> None:
    records = [active_valid_record]
    result = TimestampTransformer(timestamp="2026-07-01").process(records)

    assert result == [
        Record(
            id=1,
            name="Ada",
            status="active",
            processed=True,
            timestamp="2026-07-01",
        )
    ]
    assert result[0] is active_valid_record


def test_record_to_dict_includes_optional_processed_fields() -> None:
    record = Record(
        id=1,
        name="Ada",
        status="active",
        processed=True,
        timestamp="2026-07-01",
    )

    assert record.to_dict() == {
        "id": 1,
        "name": "Ada",
        "status": "active",
        "processed": True,
        "timestamp": "2026-07-01",
    }


def test_validator_keeps_records_with_positive_id_and_name() -> None:
    records: list[Record] = [
        Record(id=1, name="Ada"),
        Record(id=0, name="Grace"),
        Record(id=2, name=""),
        Record(id=None, name="Katherine"),
    ]

    result = RequiredFieldsValidator().process(records)

    assert result == [Record(id=1, name="Ada")]


def test_pipeline_chains_filter_transform_and_validate(records: list[Record]) -> None:
    pipeline = ProcessingPipeline(
        [
            ActiveRecordFilter(),
            TimestampTransformer(),
            RequiredFieldsValidator(),
        ]
    )

    result = pipeline.process(records)

    assert result == [
        Record(
            id=1,
            name="Ada",
            status="active",
            processed=True,
            timestamp="2024-01-01",
        )
    ]


def test_empty_pipeline_returns_original_records(records: list[Record]) -> None:
    result = ProcessingPipeline([]).process(records)

    assert result is records


@pytest.mark.parametrize(
    ("process_type", "expected_type"),
    PROCESSOR_CASES,
)
def test_processor_for_returns_expected_processor(
    process_type: ProcessType,
    expected_type: type[DataProcessor],
) -> None:
    assert isinstance(processor_for(process_type), expected_type)


def test_processor_for_rejects_unknown_process_type() -> None:
    with pytest.raises(UnsupportedProcessTypeError, match="Unsupported process type"):
        processor_for("unknown")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("bad_records", "message"),
    [
        ((Record(id=1, name="Ada"),), "provided as a list"),
        ([{"id": 1, "name": "Ada"}], "Record instances"),
    ],
)
def test_processor_validation_decorator_rejects_bad_inputs(
    bad_records: object,
    message: str,
) -> None:
    with pytest.raises(DataValidationError, match=message):
        ActiveRecordFilter().process(bad_records)  # type: ignore[arg-type]


class ExplodingProcessor(DataProcessor):
    """Processor used to verify exception wrapping."""

    def _handle(self, records: list[Record]) -> list[Record]:
        raise ValueError("broken record")


class FailingProcessor(DataProcessor):
    """Processor used to verify custom exceptions are preserved."""

    def _handle(self, records: list[Record]) -> list[Record]:
        raise DataProcessingError("already specific")


def test_processor_wraps_unexpected_processing_errors(
    active_valid_record: Record,
) -> None:
    with pytest.raises(DataProcessingError, match="failed to process records"):
        ExplodingProcessor().process([active_valid_record])


def test_processor_preserves_specific_processing_errors(
    active_valid_record: Record,
) -> None:
    with pytest.raises(DataProcessingError, match="already specific"):
        FailingProcessor().process([active_valid_record])


def test_json_record_reader_and_writer_use_context_managers(
    json_input_file: Path,
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "output.json"

    with JsonRecordReader(str(json_input_file)) as reader:
        records = reader.read()

    with JsonRecordWriter(str(output_file)) as writer:
        writer.write(records)

    assert records[0] == Record(id=1, name="Ada", status="active")
    assert json.loads(output_file.read_text())[0] == {
        "id": 1,
        "name": "Ada",
        "status": "active",
    }


@pytest.mark.parametrize(
    ("file_content", "message"),
    [
        ("{", "Invalid JSON"),
        ('{"id": 1, "name": "Ada"}', "record objects"),
        ("[1, 2, 3]", "record objects"),
    ],
)
def test_json_record_reader_rejects_invalid_input(
    tmp_path: Path,
    file_content: str,
    message: str,
) -> None:
    input_file = tmp_path / "input.json"
    input_file.write_text(file_content)

    with JsonRecordReader(str(input_file)) as reader:
        with pytest.raises(DataLoadError, match=message):
            reader.read()


def test_json_record_reader_rejects_read_before_open(tmp_path: Path) -> None:
    reader = JsonRecordReader(str(tmp_path / "input.json"))

    with pytest.raises(DataLoadError, match="opened before reading"):
        reader.read()


def test_json_record_reader_wraps_open_os_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise OSError("permission denied")

    monkeypatch.setattr(readers.Path, "open", fail_open)

    with pytest.raises(DataLoadError, match="Unable to read input file"):
        JsonRecordReader(str(tmp_path / "input.json")).__enter__()


def test_json_record_writer_rejects_write_before_open(tmp_path: Path) -> None:
    writer = JsonRecordWriter(str(tmp_path / "output.json"))

    with pytest.raises(DataSaveError, match="opened before writing"):
        writer.write([Record(id=1, name="Ada")])


def test_json_record_writer_wraps_open_os_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise OSError("read-only destination")

    monkeypatch.setattr(writers.Path, "open", fail_open)

    with pytest.raises(DataSaveError, match="Unable to open output file"):
        JsonRecordWriter(str(tmp_path / "output.json")).__enter__()


def test_json_record_writer_wraps_dump_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    active_valid_record: Record,
) -> None:
    def fail_dump(*args: object, **kwargs: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(writers.json, "dump", fail_dump)

    with JsonRecordWriter(str(tmp_path / "output.json")) as writer:
        with pytest.raises(DataSaveError, match="Unable to save results"):
            writer.write([active_valid_record])
