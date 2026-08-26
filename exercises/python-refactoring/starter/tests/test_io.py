"""Tests for safe JSON reading and atomic writing."""

import json
import logging
import os
import tempfile
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import cast

import pytest

from codex_refactoring.data_processing.models import Record
from codex_refactoring.data_processing.readers import read_json_records
from codex_refactoring.data_processing.writers import (
    serialize_records,
    write_json_records,
)
from codex_refactoring.exceptions import (
    DataReadError,
    DataWriteError,
    InvalidDataFormatError,
)


def test_reader_loads_utf8_record_array(tmp_path: Path) -> None:
    """The reader accepts a valid UTF-8 array of JSON objects."""
    source = tmp_path / "records.json"
    source.write_text('[{"id": 1, "name": "René"}]', encoding="utf-8")

    assert read_json_records(source) == [{"id": 1, "name": "René"}]


def test_reader_rejects_invalid_json(tmp_path: Path) -> None:
    """Syntax errors retain a useful path-specific exception."""
    source = tmp_path / "broken.json"
    source.write_text("[", encoding="utf-8")

    with pytest.raises(DataReadError, match="Invalid JSON.*broken.json"):
        read_json_records(source)


def test_reader_wraps_file_and_encoding_errors(tmp_path: Path) -> None:
    """Missing files and invalid UTF-8 are reported as read errors."""
    with pytest.raises(DataReadError, match="Unable to read"):
        read_json_records(tmp_path / "missing.json")

    invalid_utf8 = tmp_path / "invalid.json"
    invalid_utf8.write_bytes(b"\xff")
    with pytest.raises(DataReadError, match="Unable to read"):
        read_json_records(invalid_utf8)


def test_reader_requires_array_at_document_root(tmp_path: Path) -> None:
    """A top-level object is not silently treated as an iterable of keys."""
    source = tmp_path / "object.json"
    source.write_text('{"id": 1}', encoding="utf-8")

    with pytest.raises(InvalidDataFormatError, match="Expected a JSON array"):
        read_json_records(source)


def test_reader_requires_objects_in_array(tmp_path: Path) -> None:
    """Each array item must be a record object."""
    source = tmp_path / "mixed.json"
    source.write_text('[{"id": 1}, 2]', encoding="utf-8")

    with pytest.raises(InvalidDataFormatError, match="object at index 1"):
        read_json_records(source)


def test_writer_serializes_before_atomically_replacing_destination(
    tmp_path: Path,
) -> None:
    """A successful write is formatted, Unicode-safe, and leaves no temp file."""
    destination = tmp_path / "results.json"
    destination.write_text("old content", encoding="utf-8")
    records: list[Record] = [{"id": 1, "name": "René"}]

    write_json_records(records, destination)

    assert json.loads(destination.read_text(encoding="utf-8")) == records
    assert "René" in destination.read_text(encoding="utf-8")
    assert list(tmp_path.glob(".results.json.*.tmp")) == []


@pytest.mark.parametrize("bad_value", [float("nan"), object()])
def test_serialization_failures_do_not_touch_destination(
    tmp_path: Path, bad_value: object
) -> None:
    """Non-JSON values fail before an existing output file is opened."""
    destination = tmp_path / "results.json"
    destination.write_text("preserve me", encoding="utf-8")
    records = [cast(Record, {"value": bad_value})]

    with pytest.raises(DataWriteError, match="Unable to serialize"):
        write_json_records(records, destination)

    assert destination.read_text(encoding="utf-8") == "preserve me"


def test_writer_reports_unusable_destination(tmp_path: Path) -> None:
    """Filesystem failures are wrapped without claiming an empty result."""
    destination = tmp_path / "missing" / "results.json"

    with pytest.raises(DataWriteError, match="Unable to write"):
        write_json_records([], destination)


def test_writer_wraps_permission_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Permission failures are exposed as application write errors."""

    def deny_temporary_file(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise PermissionError("permission denied")

    monkeypatch.setattr(tempfile, "NamedTemporaryFile", deny_temporary_file)

    with pytest.raises(DataWriteError, match="permission denied"):
        write_json_records([], tmp_path / "output.json")


def test_writer_removes_temporary_file_after_fsync_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A durability failure leaves neither partial output nor temporary residue."""
    destination = tmp_path / "results.json"

    def fail_fsync(file_descriptor: int) -> None:
        del file_descriptor
        raise OSError("disk full")

    monkeypatch.setattr(os, "fsync", fail_fsync)

    with pytest.raises(DataWriteError, match="disk full"):
        write_json_records([{"id": 1}], destination)

    assert not destination.exists()
    assert list(tmp_path.glob(".results.json.*.tmp")) == []


def test_writer_cleans_up_after_atomic_replace_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A failed replacement attempts cleanup and reports cleanup failures."""
    destination = tmp_path / "results.json"

    def fail_replace(self: Path, target: Path) -> Path:
        del self, target
        raise OSError("replace failed")

    def fail_unlink(self: Path) -> None:
        del self
        raise OSError("unlink failed")

    monkeypatch.setattr(Path, "replace", fail_replace)
    monkeypatch.setattr(Path, "unlink", fail_unlink)
    caplog.set_level(logging.WARNING)

    with pytest.raises(DataWriteError, match="replace failed"):
        write_json_records([], destination)

    assert "Unable to remove temporary file" in caplog.text


def test_serialize_records_accepts_generators() -> None:
    """Serialization materializes one-shot record iterables exactly once."""
    records: Iterable[Record] = ({"id": record_id} for record_id in range(2))
    assert json.loads(serialize_records(records)) == [{"id": 0}, {"id": 1}]


def test_concurrent_writes_never_produce_partial_json(tmp_path: Path) -> None:
    """Competing atomic writers leave one complete payload and no temp files."""
    destination = tmp_path / "shared.json"
    payloads: list[list[Record]] = [
        [{"writer": writer_id, "values": list(range(writer_id + 1))}]
        for writer_id in range(8)
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        list(
            executor.map(
                lambda payload: write_json_records(payload, destination), payloads
            )
        )

    final_payload = json.loads(destination.read_text(encoding="utf-8"))
    assert final_payload in payloads
    assert list(tmp_path.glob(".shared.json.*.tmp")) == []
