"""Integration tests for the processing pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from legacy_processor import run_pipeline


def test_pipeline_end_to_end(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.json"

    input_path.write_text(
        json.dumps(
            [
                {"id": 1, "name": "Ada", "status": "active"},
                {"id": 2, "name": "Bob", "status": "inactive"},
                {"id": -1, "name": "Bad", "status": "active"},
            ]
        )
    )

    count = run_pipeline(input_path, output_path)

    assert count == 1
    result = json.loads(output_path.read_text())
    assert result[0]["id"] == 1
    assert result[0]["processed"] is True
