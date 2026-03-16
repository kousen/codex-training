"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sample_payload() -> list[dict[str, object]]:
    """Return representative raw records."""

    return [
        {"id": 1, "name": "Alpha", "status": "active", "category": "gold"},
        {"id": 2, "name": "Beta", "status": "inactive"},
        {"id": 3, "name": "Gamma", "status": "active"},
    ]


@pytest.fixture
def input_json_file(tmp_path: Path) -> Path:
    """Write sample payload to a temporary JSON file."""

    input_path = tmp_path / "input.json"
    input_path.write_text(
        (
            "["
            '{"id": 1, "name": "Alpha", "status": "active", "category": "gold"},'
            '{"id": 2, "name": "Beta", "status": "inactive"},'
            '{"id": 3, "name": "Gamma", "status": "active"}'
            "]"
        ),
        encoding="utf-8",
    )
    return input_path
