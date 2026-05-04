"""Shared pytest fixtures for the refactored data processor."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def sample_records() -> list[dict[str, Any]]:
    """Return representative raw records for processing tests."""

    return [
        {"id": 1, "name": "Ada", "status": "active", "team": "math"},
        {"id": 2, "name": "Grace", "status": "inactive"},
        {"id": 0, "name": "", "status": "active"},
    ]


@pytest.fixture
def json_file(tmp_path: Path, sample_records: list[dict[str, Any]]) -> Path:
    """Create a JSON input file with representative records."""

    path = tmp_path / "input.json"
    path.write_text(
        """
[
  {"id": 1, "name": "Ada", "status": "active", "team": "math"},
  {"id": 2, "name": "Grace", "status": "inactive"},
  {"id": 0, "name": "", "status": "active"}
]
""".strip(),
        encoding="utf-8",
    )
    return path


@pytest.fixture
def unreadable_path(tmp_path: Path) -> Iterator[Path]:
    """Yield a path that disappears before it can be read."""

    path = tmp_path / "missing.json"
    yield path
