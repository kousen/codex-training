"""Integration tests for the compatibility entry point."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import legacy_processor
from exceptions.custom import WriterError


def test_process_wrapper_delegates(sample_records: list[dict[str, object]]) -> None:
    """Legacy process wrapper delegates to typed processing."""

    assert [
        record["id"] for record in legacy_processor.process(sample_records, "filter")
    ] == [
        1,
        0,
    ]


def test_load_and_process_returns_empty_list_on_domain_error(
    unreadable_path: Path,
) -> None:
    """Compatibility loader preserves the legacy empty-list fallback."""

    assert legacy_processor.load_and_process(unreadable_path, "filter") == []


def test_load_and_process_reads_valid_file(json_file: Path) -> None:
    """Compatibility loader processes valid files."""

    assert [
        record["id"]
        for record in legacy_processor.load_and_process(json_file, "filter")
    ] == [
        1,
        0,
    ]


def test_save_results_writes_file(tmp_path: Path) -> None:
    """Compatibility writer delegates to JSON writer."""

    output_path = tmp_path / "output.json"
    legacy_processor.save_results([{"id": 1}], output_path)

    assert json.loads(output_path.read_text(encoding="utf-8")) == [{"id": 1}]


def test_save_results_raises_writer_errors(tmp_path: Path) -> None:
    """Compatibility writer keeps specific writer errors visible."""

    with pytest.raises(WriterError):
        legacy_processor.save_results([{"bad": object()}], tmp_path / "output.json")


def test_main_processes_cli_arguments(json_file: Path, tmp_path: Path) -> None:
    """CLI returns success and writes output for valid files."""

    output_path = tmp_path / "output.json"

    assert (
        legacy_processor.main(["--input", str(json_file), "--output", str(output_path)])
        == 0
    )
    assert json.loads(output_path.read_text(encoding="utf-8"))[0]["id"] == 1


def test_main_returns_failure_for_missing_input(
    unreadable_path: Path, tmp_path: Path
) -> None:
    """CLI converts domain errors into a non-zero exit code."""

    assert (
        legacy_processor.main(
            ["--input", str(unreadable_path), "--output", str(tmp_path / "output.json")]
        )
        == 1
    )
