"""Integration tests for the legacy compatibility layer."""

from __future__ import annotations

import logging
import runpy
from pathlib import Path

import legacy_processor
import pytest

from data_processing.models import ProcessingRecord
from exceptions.custom import DataLoadError


def test_process_function(sample_payload: list[dict[str, object]]) -> None:
    result = legacy_processor.process(sample_payload, "filter")

    assert [item["id"] for item in result] == [1, 3]


def test_load_and_process(input_json_file: Path) -> None:
    result = legacy_processor.load_and_process(input_json_file, "validate")

    assert [item["id"] for item in result] == [1, 2, 3]


def test_save_results_round_trip(tmp_path: Path) -> None:
    output_path = tmp_path / "output.json"
    legacy_processor.save_results(
        [{"id": 1, "name": "Alpha", "status": "active"}],
        output_path,
    )

    assert output_path.exists()
    assert '"processed": false' in output_path.read_text(encoding="utf-8").lower()


def test_build_parser_defaults() -> None:
    parser = legacy_processor.build_parser()
    args = parser.parse_args([])

    assert args.input == legacy_processor.DEFAULT_INPUT_FILE
    assert args.output == legacy_processor.DEFAULT_OUTPUT_FILE
    assert args.log_level == "INFO"


def test_main_returns_error_for_missing_input(tmp_path: Path) -> None:
    missing_input = tmp_path / "missing.json"

    assert legacy_processor.main(["--input", str(missing_input)]) == 1


def test_main_returns_error_when_pipeline_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text("[]", encoding="utf-8")

    def raise_error(input_file: str, output_file: str) -> list[object]:
        raise DataLoadError(f"broken: {input_file} -> {output_file}")

    monkeypatch.setattr(legacy_processor, "run_pipeline", raise_error)

    assert legacy_processor.main(["--input", str(input_path)]) == 1


def test_main_success(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text("[]", encoding="utf-8")
    output_path = tmp_path / "output.json"

    monkeypatch.setattr(
        legacy_processor,
        "run_pipeline",
        lambda *_args: [object(), object()],
    )

    exit_code = legacy_processor.main(
        [
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--log-level",
            "DEBUG",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Done! Processed 2 items" in captured.out


def test_run_pipeline_uses_default_modes(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class StubPipeline:
        def __init__(self, logger: logging.Logger) -> None:
            captured["logger_name"] = logger.name

        def process_file(
            self, input_path: str, output_path: str, modes: tuple[object, ...]
        ) -> list[ProcessingRecord]:
            captured["input_path"] = input_path
            captured["output_path"] = output_path
            captured["modes"] = modes
            return [ProcessingRecord(name="ok")]

    monkeypatch.setattr(legacy_processor, "DataProcessingPipeline", StubPipeline)

    result = legacy_processor.run_pipeline("input.json", "output.json")

    assert len(result) == 1
    assert result[0].name == "ok"
    assert captured["input_path"] == "input.json"
    assert captured["output_path"] == "output.json"
    assert captured["modes"] == legacy_processor.DEFAULT_PIPELINE


def test_module_main_entrypoint(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["legacy_processor.py", "--input", str(input_path)],
    )
    monkeypatch.setattr(legacy_processor, "run_pipeline", lambda *_args: [])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("legacy_processor", run_name="__main__")

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "Done! Processed 0 items" in captured.out
