"""Compatibility tests for the legacy module facade."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

import legacy_processor
from legacy_processor import load_and_process, process, save_results
from src.data_processing import Record
from src.data_processing.processors import ProcessType
from src.exceptions import DataLoadError, DataProcessingError

PROCESS_CASES: list[tuple[ProcessType, list[Record]]] = [
    (
        "filter",
        [
            Record(id=1, name="Ada", status="active"),
            Record(id=0, name="Barbara", status="active"),
            Record(id=3, name="", status="active"),
        ],
    ),
    (
        "transform",
        [
            Record(
                id=1,
                name="Ada",
                status="active",
                processed=True,
                timestamp="2024-01-01",
            ),
            Record(
                id=2,
                name="Grace",
                status="inactive",
                processed=True,
                timestamp="2024-01-01",
            ),
            Record(
                id=0,
                name="Barbara",
                status="active",
                processed=True,
                timestamp="2024-01-01",
            ),
            Record(
                id=3,
                name="",
                status="active",
                processed=True,
                timestamp="2024-01-01",
            ),
        ],
    ),
    (
        "validate",
        [
            Record(id=1, name="Ada", status="active"),
            Record(id=2, name="Grace", status="inactive"),
        ],
    ),
]


@pytest.mark.parametrize(
    ("process_type", "expected"),
    PROCESS_CASES,
)
def test_legacy_process_delegates_to_processor(
    raw_records: list[dict[str, object]],
    process_type: ProcessType,
    expected: list[Record],
) -> None:
    assert process(raw_records, process_type) == expected


def test_legacy_load_and_process_reads_json(json_input_file: Path) -> None:
    assert load_and_process(str(json_input_file), "filter") == [
        Record(id=1, name="Ada", status="active"),
        Record(id=0, name="Barbara", status="active"),
        Record(id=3, name="", status="active"),
    ]


def test_legacy_load_and_process_raises_custom_error_for_missing_file(
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(DataLoadError, match="Input file not found"):
        load_and_process(str(missing_file), "filter")


def test_legacy_load_and_process_raises_custom_error_for_invalid_json(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "input.json"
    input_file.write_text("{")

    with pytest.raises(DataLoadError, match="Invalid JSON"):
        load_and_process(str(input_file), "filter")


def test_legacy_save_results_writes_json(
    tmp_path: Path,
    active_valid_record: Record,
) -> None:
    output_file = tmp_path / "output.json"

    save_results([active_valid_record], str(output_file))

    assert json.loads(output_file.read_text()) == [
        {"id": 1, "name": "Ada", "status": "active"}
    ]


def test_legacy_main_warns_when_input_file_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setattr(legacy_processor.os.path, "exists", lambda filename: False)

    with caplog.at_level(logging.WARNING, logger="legacy_processor"):
        legacy_processor.main()

    assert "File not found: /tmp/input.json" in caplog.text


def test_legacy_main_processes_existing_input(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    saved_records: list[Record] = []

    monkeypatch.setattr(legacy_processor.os.path, "exists", lambda filename: True)
    monkeypatch.setattr(
        legacy_processor,
        "load_records",
        lambda filename: [Record(id=1, name="Ada", status="active")],
    )
    monkeypatch.setattr(
        legacy_processor,
        "save_results",
        lambda records, filename: saved_records.extend(records),
    )

    with caplog.at_level(logging.INFO, logger="legacy_processor"):
        legacy_processor.main()

    assert saved_records == [
        Record(
            id=1,
            name="Ada",
            status="active",
            processed=True,
            timestamp="2024-01-01",
        )
    ]
    assert "Done! Processed 1 items" in caplog.text


def test_legacy_main_logs_processing_errors(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    def fail_load(filename: str) -> list[Record]:
        raise DataProcessingError("boom")

    monkeypatch.setattr(legacy_processor.os.path, "exists", lambda filename: True)
    monkeypatch.setattr(legacy_processor, "load_records", fail_load)

    with caplog.at_level(logging.ERROR, logger="legacy_processor"):
        legacy_processor.main()

    assert "Processing failed: boom" in caplog.text
