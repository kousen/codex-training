"""Integration tests for the legacy entrypoint."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import pytest

import legacy_processor
from exceptions.custom import DataProcessingError


def test_main_logs_missing_file(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing_path = tmp_path / "missing.json"
    monkeypatch.setattr(legacy_processor, "INPUT_FILE", missing_path)

    with caplog.at_level("ERROR"):
        legacy_processor.main()

    assert "Input file not found" in caplog.text


def test_main_handles_processing_error(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps([{"id": 1, "name": "Ada", "status": "active"}]))
    monkeypatch.setattr(legacy_processor, "INPUT_FILE", input_path)
    monkeypatch.setattr(legacy_processor, "OUTPUT_FILE", tmp_path / "output.json")

    def raise_error(*args: object, **kwargs: object) -> int:
        raise DataProcessingError("boom")

    monkeypatch.setattr(legacy_processor, "run_pipeline", raise_error)

    with caplog.at_level("ERROR"):
        legacy_processor.main()

    assert "Processing failed" in caplog.text


def test_main_success_writes_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.json"
    input_path.write_text(
        json.dumps([
            {"id": 1, "name": "Ada", "status": "active"},
            {"id": 2, "name": "Bob", "status": "inactive"},
        ])
    )

    monkeypatch.setattr(legacy_processor, "INPUT_FILE", input_path)
    monkeypatch.setattr(legacy_processor, "OUTPUT_FILE", output_path)

    legacy_processor.main()

    assert output_path.exists()
    payload = json.loads(output_path.read_text())
    assert payload[0]["processed"] is True


def test_module_runs_as_main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    script_path = project_root / "legacy_processor.py"
    input_path = Path("/tmp/input.json")
    output_path = Path("/tmp/output.json")

    original_input = (
        input_path.read_text(encoding="utf-8") if input_path.exists() else None
    )
    original_output = (
        output_path.read_text(encoding="utf-8") if output_path.exists() else None
    )

    try:
        input_path.write_text(
            json.dumps([
                {"id": 1, "name": "Ada", "status": "active"},
            ]),
            encoding="utf-8",
        )
        runpy.run_path(str(script_path), run_name="__main__")
        assert output_path.exists()
    finally:
        if original_input is None and input_path.exists():
            input_path.unlink()
        elif original_input is not None:
            input_path.write_text(original_input, encoding="utf-8")

        if original_output is None and output_path.exists():
            output_path.unlink()
        elif original_output is not None:
            output_path.write_text(original_output, encoding="utf-8")
