"""Compatibility tests for the legacy module facade."""

import json
from pathlib import Path

from legacy_processor import load_and_process, process, save_results
from src.data_processing import Record


def test_legacy_process_delegates_to_processor() -> None:
    records: list[Record] = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
    ]

    assert process(records, "filter") == [{"id": 1, "name": "Ada", "status": "active"}]


def test_legacy_load_and_process_reads_json(tmp_path: Path) -> None:
    input_file = tmp_path / "input.json"
    input_file.write_text(
        json.dumps(
            [
                {"id": 1, "name": "Ada", "status": "active"},
                {"id": 2, "name": "Grace", "status": "inactive"},
            ]
        )
    )

    assert load_and_process(str(input_file), "filter") == [
        {"id": 1, "name": "Ada", "status": "active"}
    ]


def test_legacy_save_results_writes_json(tmp_path: Path) -> None:
    output_file = tmp_path / "output.json"
    records: list[Record] = [{"id": 1, "name": "Ada"}]

    save_results(records, str(output_file))

    assert json.loads(output_file.read_text()) == records
