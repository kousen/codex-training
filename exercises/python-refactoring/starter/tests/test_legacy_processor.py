"""Integration and command-line tests for the compatibility module."""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

import legacy_processor
from codex_refactoring.data_processing.models import Record
from codex_refactoring.exceptions import DataReadError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUCCESS_EXIT_CODE = 0
FAILURE_EXIT_CODE = 1


def fixed_clock() -> datetime:
    """Return a deterministic UTC timestamp."""
    return datetime(2026, 8, 26, 15, 30, tzinfo=timezone.utc)


def write_input(path: Path) -> list[Record]:
    """Write and return representative active and inactive records."""
    records: list[Record] = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
    ]
    path.write_text(json.dumps(records), encoding="utf-8")
    return records


def test_legacy_process_wrapper() -> None:
    """The old process name remains available with the safer behavior."""
    record: Record = {"id": 1, "name": "Ada"}
    result = legacy_processor.process([record], "transform", clock=fixed_clock)
    assert result[0]["processed"] is True
    assert "processed" not in record


def test_load_and_process_wrapper(tmp_path: Path) -> None:
    """The old load-and-process name composes reader and strategy."""
    source = tmp_path / "input.json"
    records = write_input(source)
    assert legacy_processor.load_and_process(source, "filter") == [records[0]]


def test_save_results_wrapper(tmp_path: Path) -> None:
    """The old save name delegates to atomic JSON output."""
    output = tmp_path / "output.json"
    legacy_processor.save_results([{"id": 1}], output)
    assert json.loads(output.read_text(encoding="utf-8")) == [{"id": 1}]


def test_run_pipeline_supports_configurable_operations(tmp_path: Path) -> None:
    """Callers can choose and order operations rather than using a fixed main."""
    source = tmp_path / "input.json"
    output = tmp_path / "output.json"
    records = write_input(source)

    result = legacy_processor.run_pipeline(
        source, output, ["filter", "validate"], clock=fixed_clock
    )

    assert result == [records[0]]
    assert json.loads(output.read_text(encoding="utf-8")) == result


def test_main_runs_default_pipeline(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """The CLI reports success and produces default-pipeline output."""
    source = tmp_path / "input.json"
    output = tmp_path / "output.json"
    write_input(source)
    caplog.set_level(logging.INFO)

    exit_code = legacy_processor.main([str(source), str(output), "--verbose"])

    assert exit_code == 0
    assert json.loads(output.read_text(encoding="utf-8"))[0]["processed"] is True
    assert "Processed 1 items" in caplog.text


def test_main_returns_failure_for_expected_application_error(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Expected failures have a nonzero exit code and an actionable log."""
    caplog.set_level(logging.ERROR)

    exit_code = legacy_processor.main(
        [str(tmp_path / "missing.json"), str(tmp_path / "output.json")]
    )

    assert exit_code == 1
    assert "Processing failed" in caplog.text


def test_load_and_process_propagates_read_errors(tmp_path: Path) -> None:
    """Read failures are distinguishable from legitimate empty datasets."""
    with pytest.raises(DataReadError):
        legacy_processor.load_and_process(tmp_path / "missing.json", "filter")


def test_parser_rejects_unknown_cli_operation() -> None:
    """Argparse validates operation choices before running the pipeline."""
    argparse_error_exit_code = 2
    with pytest.raises(SystemExit) as error:
        legacy_processor.main(["input.json", "output.json", "--operations", "bad"])
    assert error.value.code == argparse_error_exit_code


def test_real_cli_subprocess_succeeds(tmp_path: Path) -> None:
    """The actual script returns zero, logs to stderr, and writes valid output."""
    source = tmp_path / "input.json"
    output = tmp_path / "output.json"
    write_input(source)
    environment = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")}

    completed = subprocess.run(
        [sys.executable, "legacy_processor.py", str(source), str(output)],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == SUCCESS_EXIT_CODE
    assert "INFO: Processed 1 items" in completed.stderr
    assert json.loads(output.read_text(encoding="utf-8"))[0]["name"] == "Ada"


def test_real_cli_subprocess_reports_failure(tmp_path: Path) -> None:
    """The actual script exposes expected failures through status and stderr."""
    output = tmp_path / "output.json"
    environment = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")}

    completed = subprocess.run(
        [
            sys.executable,
            "legacy_processor.py",
            str(tmp_path / "missing.json"),
            str(output),
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == FAILURE_EXIT_CODE
    assert "ERROR: Processing failed" in completed.stderr
    assert not output.exists()


def test_empty_programmatic_pipeline_copies_and_writes_input(tmp_path: Path) -> None:
    """An explicitly empty API pipeline acts as a safe identity operation."""
    source = tmp_path / "input.json"
    output = tmp_path / "output.json"
    records = write_input(source)

    result = legacy_processor.run_pipeline(source, output, [])

    assert result == records
    assert result[0] is not records[0]
    assert json.loads(output.read_text(encoding="utf-8")) == records
