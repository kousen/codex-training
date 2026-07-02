"""Shared pytest fixtures for the refactoring exercise test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from src.data_processing import Record


@pytest.fixture
def raw_records() -> list[dict[str, Any]]:
    """Return JSON-style records that exercise filter, transform, and validation."""
    return [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
        {"id": 0, "name": "Barbara", "status": "active"},
        {"id": 3, "name": "", "status": "active"},
    ]


@pytest.fixture
def records(raw_records: list[dict[str, Any]]) -> list[Record]:
    """Return dataclass records built from the common raw fixture."""
    return [Record.from_mapping(raw_record) for raw_record in raw_records]


@pytest.fixture
def active_valid_record() -> Record:
    """Return one record that should pass the default processing pipeline."""
    return Record(id=1, name="Ada", status="active")


@pytest.fixture
def json_input_file(tmp_path: Path, raw_records: list[dict[str, Any]]) -> Path:
    """Write the common raw records to a temporary JSON input file."""
    input_file = tmp_path / "input.json"
    input_file.write_text(json.dumps(raw_records))
    return input_file
