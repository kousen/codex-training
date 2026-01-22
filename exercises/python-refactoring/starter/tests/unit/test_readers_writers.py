"""Unit tests for file readers and writers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_processing.models import Record
from data_processing.readers import read_json_records
from data_processing.writers import write_json_records
from exceptions.custom import DataLoadError, DataValidationError, DataWriteError


def test_read_json_records_success(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(
        json.dumps(
            [
                {"id": 1, "name": "Ada", "status": "active"},
                {"id": 2, "name": "Bob", "status": "inactive"},
            ]
        )
    )

    records = read_json_records(input_path)

    assert len(records) == 2
    assert records[0].record_id == 1


def test_read_json_records_rejects_non_list(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps({"id": 1, "name": "Ada"}))

    with pytest.raises(DataValidationError):
        read_json_records(input_path)


def test_read_json_records_rejects_invalid_json(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text("not-json")

    with pytest.raises(DataLoadError):
        read_json_records(input_path)


def test_read_json_records_rejects_non_mapping_items(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps([1, 2, 3]))

    with pytest.raises(DataValidationError):
        read_json_records(input_path)


def test_write_json_records_round_trip(tmp_path: Path) -> None:
    output_path = tmp_path / "output.json"
    records = [Record(record_id=1, name="Ada", status="active")]

    write_json_records(output_path, records)
    raw = json.loads(output_path.read_text())

    assert raw == [{"id": 1, "name": "Ada", "status": "active", "processed": False}]


def test_write_json_records_raises_on_os_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_path = tmp_path / "output.json"
    records = [Record(record_id=1, name="Ada", status="active")]

    def raise_os_error(*args: object, **kwargs: object) -> None:
        raise OSError("nope")

    monkeypatch.setattr(Path, "open", raise_os_error)

    with pytest.raises(DataWriteError):
        write_json_records(output_path, records)
