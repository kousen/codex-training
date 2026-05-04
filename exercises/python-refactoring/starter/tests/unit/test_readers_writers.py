"""Unit tests for JSON readers and writers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import NoReturn

import pytest

from data_processing.readers import JsonFileReader
from data_processing.writers import JsonFileWriter
from exceptions.custom import InvalidDataError, ReaderError, WriterError


def test_json_file_reader_reads_list(json_file: Path) -> None:
    """Reader loads a JSON array of objects."""

    records = JsonFileReader().read(json_file)

    assert records[0]["name"] == "Ada"


def test_json_file_reader_rejects_missing_file(unreadable_path: Path) -> None:
    """Missing files raise a specific reader error."""

    with pytest.raises(ReaderError, match="not found"):
        JsonFileReader().read(unreadable_path)


def test_json_file_reader_rejects_invalid_json(tmp_path: Path) -> None:
    """Malformed JSON raises a specific reader error."""

    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ReaderError, match="invalid JSON"):
        JsonFileReader().read(path)


def test_json_file_reader_wraps_permission_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Permission failures are wrapped in a reader error."""

    def raise_permission_error(
        self: Path,
        mode: str = "r",
        encoding: str | None = None,
    ) -> NoReturn:
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "open", raise_permission_error)

    with pytest.raises(ReaderError, match="not readable"):
        JsonFileReader().read(tmp_path / "secret.json")


def test_json_file_reader_wraps_other_os_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Unexpected OS failures are wrapped in a reader error."""

    def raise_os_error(
        self: Path,
        mode: str = "r",
        encoding: str | None = None,
    ) -> NoReturn:
        raise OSError("disk unavailable")

    monkeypatch.setattr(Path, "open", raise_os_error)

    with pytest.raises(ReaderError, match="Could not read"):
        JsonFileReader().read(tmp_path / "input.json")


def test_json_file_reader_rejects_non_list(tmp_path: Path) -> None:
    """JSON roots must be arrays."""

    path = tmp_path / "object.json"
    path.write_text('{"id": 1}', encoding="utf-8")

    with pytest.raises(InvalidDataError, match="list"):
        JsonFileReader().read(path)


def test_json_file_reader_rejects_non_objects(tmp_path: Path) -> None:
    """Every array item must be an object."""

    path = tmp_path / "array.json"
    path.write_text("[1]", encoding="utf-8")

    with pytest.raises(InvalidDataError, match="object"):
        JsonFileReader().read(path)


def test_json_file_writer_writes_indented_json(tmp_path: Path) -> None:
    """Writer emits JSON that can be read back."""

    path = tmp_path / "output.json"
    JsonFileWriter().write([{"id": 1, "name": "Ada"}], path)

    assert json.loads(path.read_text(encoding="utf-8")) == [{"id": 1, "name": "Ada"}]
    assert path.read_text(encoding="utf-8").endswith("\n")


def test_json_file_writer_wraps_serialization_errors(tmp_path: Path) -> None:
    """Non-serializable data raises a writer error."""

    path = tmp_path / "output.json"

    with pytest.raises(WriterError, match="Could not write"):
        JsonFileWriter().write([{"bad": object()}], path)
