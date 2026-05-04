"""Integration tests for the data-processing pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_processing.pipeline import DataProcessingPipeline, load_process_save
from exceptions.custom import ReaderError


def test_pipeline_processes_file(json_file: Path, tmp_path: Path) -> None:
    """The high-level pipeline reads, processes, and writes records."""

    output_path = tmp_path / "output.json"

    count = DataProcessingPipeline().process_file(json_file, output_path)

    assert count == 1
    assert json.loads(output_path.read_text(encoding="utf-8")) == [
        {
            "id": 1,
            "name": "Ada",
            "status": "active",
            "processed": True,
            "timestamp": "2024-01-01",
            "team": "math",
        }
    ]


def test_load_process_save_uses_custom_timestamp(
    json_file: Path, tmp_path: Path
) -> None:
    """Functional helper accepts timestamp customization."""

    output_path = tmp_path / "output.json"

    assert load_process_save(json_file, output_path, timestamp="today") == 1
    assert (
        json.loads(output_path.read_text(encoding="utf-8"))[0]["timestamp"] == "today"
    )


def test_pipeline_propagates_domain_errors(
    unreadable_path: Path, tmp_path: Path
) -> None:
    """Pipeline does not hide reader failures."""

    with pytest.raises(ReaderError):
        DataProcessingPipeline().process_file(unreadable_path, tmp_path / "out.json")
