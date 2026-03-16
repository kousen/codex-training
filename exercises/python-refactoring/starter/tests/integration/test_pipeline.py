"""Integration tests for the processing pipeline."""

from __future__ import annotations

import logging
from pathlib import Path

from data_processing.models import ProcessingRecord
from data_processing.pipeline import DataProcessingPipeline
from data_processing.processors import ProcessingMode


def test_pipeline_process_records_in_order() -> None:
    logger = logging.getLogger("pipeline-test")
    pipeline = DataProcessingPipeline(logger)
    records = [
        ProcessingRecord(id=1, name="Alpha", status="active"),
        ProcessingRecord(id=2, name="", status="active"),
        ProcessingRecord(id=3, name="Gamma", status="inactive"),
    ]

    result = pipeline.process_records(
        records,
        [ProcessingMode.FILTER, ProcessingMode.TRANSFORM, ProcessingMode.VALIDATE],
    )

    assert [record.id for record in result] == [1]
    assert result[0].processed is True
    assert result[0].timestamp == "2024-01-01"


def test_pipeline_process_file(input_json_file: Path, tmp_path: Path) -> None:
    logger = logging.getLogger("pipeline-file")
    pipeline = DataProcessingPipeline(logger)
    output_path = tmp_path / "output.json"

    result = pipeline.process_file(
        str(input_json_file),
        str(output_path),
        [ProcessingMode.FILTER, ProcessingMode.TRANSFORM, ProcessingMode.VALIDATE],
    )

    assert [record.id for record in result] == [1, 3]
    assert output_path.exists()


def test_pipeline_returns_original_records_when_no_modes_supplied() -> None:
    logger = logging.getLogger("pipeline-empty")
    pipeline = DataProcessingPipeline(logger)
    records = [ProcessingRecord(id=1, name="Alpha", status="active")]

    result = pipeline.process_records(records, [])

    assert result == records
