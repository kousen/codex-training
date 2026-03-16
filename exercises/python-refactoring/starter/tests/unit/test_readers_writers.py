"""Tests for file readers and writers."""

from __future__ import annotations

from pathlib import Path

import pytest

from data_processing.readers import JsonRecordReader
from data_processing.writers import JsonRecordWriter
from exceptions.custom import DataLoadError, DataSaveError


def test_reader_reads_records(input_json_file: Path) -> None:
    with JsonRecordReader(input_json_file) as reader:
        records = reader.read()

    assert reader.path == input_json_file
    assert [record.name for record in records] == ["Alpha", "Beta", "Gamma"]
    reader.__exit__(None, None, None)


def test_reader_raises_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(DataLoadError, match="Input file not found"):
        JsonRecordReader(missing_file).read()


def test_reader_raises_for_invalid_json(tmp_path: Path) -> None:
    input_file = tmp_path / "bad.json"
    input_file.write_text("{bad json", encoding="utf-8")

    with pytest.raises(DataLoadError, match="Invalid JSON"):
        JsonRecordReader(input_file).read()


def test_reader_wraps_generic_os_errors(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    reader = JsonRecordReader(tmp_path / "input.json")

    def raise_os_error(*args: object, **kwargs: object) -> None:
        raise OSError("permission denied")

    monkeypatch.setattr(Path, "open", raise_os_error)

    with pytest.raises(DataLoadError, match="Unable to read input file"):
        reader.read()


def test_reader_raises_for_non_list_payload(tmp_path: Path) -> None:
    input_file = tmp_path / "object.json"
    input_file.write_text('{"id": 1}', encoding="utf-8")

    with pytest.raises(DataLoadError, match="must contain a list"):
        JsonRecordReader(input_file).read()


def test_reader_raises_for_invalid_record(tmp_path: Path) -> None:
    input_file = tmp_path / "records.json"
    input_file.write_text("[1]", encoding="utf-8")

    with pytest.raises(DataLoadError, match="invalid record"):
        JsonRecordReader(input_file).read()


def test_writer_persists_records(tmp_path: Path, input_json_file: Path) -> None:
    records = JsonRecordReader(input_json_file).read()
    output_file = tmp_path / "nested" / "output.json"

    with JsonRecordWriter(output_file) as writer:
        writer.write(records)

    assert writer.path == output_file
    assert '"name": "Alpha"' in output_file.read_text(encoding="utf-8")
    writer.__exit__(None, None, None)


def test_writer_wraps_os_errors(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    writer = JsonRecordWriter(tmp_path / "output.json")

    def raise_os_error(*args: object, **kwargs: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(Path, "mkdir", raise_os_error)

    with pytest.raises(DataSaveError, match="Unable to write output file"):
        writer.write([])
