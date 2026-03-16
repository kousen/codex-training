"""Compatibility entrypoint for the refactored data processor."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from data_processing.models import ProcessingRecord
from data_processing.pipeline import DataProcessingPipeline
from data_processing.processors import ProcessingMode, ProcessorFactory
from data_processing.readers import JsonRecordReader
from data_processing.writers import JsonRecordWriter
from exceptions.custom import DataLoadError, DataProcessingError, DataSaveError
from utils.logging import configure_logging, log_exceptions

DEFAULT_INPUT_FILE = "/tmp/input.json"
DEFAULT_OUTPUT_FILE = "/tmp/output.json"
DEFAULT_PIPELINE = (
    ProcessingMode.FILTER,
    ProcessingMode.TRANSFORM,
    ProcessingMode.VALIDATE,
)

LOGGER = configure_logging()


def process(
    records: list[dict[str, Any]], process_type: ProcessingMode | str
) -> list[dict[str, Any]]:
    """Process plain dictionaries with a single strategy.

    Args:
        records: Untrusted input dictionaries.
        process_type: Processing mode to run.

    Returns:
        Processed records as plain dictionaries.
    """

    domain_records = [ProcessingRecord.from_mapping(record) for record in records]
    handler = ProcessorFactory.create(process_type)
    return [record.to_dict() for record in handler.handle(domain_records)]


@log_exceptions(LOGGER)
def load_and_process(
    file_path: str | Path, process_type: ProcessingMode | str
) -> list[dict[str, Any]]:
    """Load records from disk and process them with one strategy.

    Args:
        file_path: JSON file containing a list of records.
        process_type: Processor mode to apply.

    Returns:
        Processed records as plain dictionaries.

    Raises:
        DataLoadError: If the input file cannot be loaded.
        DataProcessingError: If processing fails.
    """

    with JsonRecordReader(file_path) as reader:
        records = reader.read()

    handler = ProcessorFactory.create(process_type)
    return [record.to_dict() for record in handler.handle(records)]


@log_exceptions(LOGGER)
def save_results(data: list[dict[str, Any]], filename: str | Path) -> None:
    """Persist processed dictionaries as JSON."""

    records = [ProcessingRecord.from_mapping(record) for record in data]
    with JsonRecordWriter(filename) as writer:
        writer.write(records)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_FILE,
        help="Path to the input JSON file.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help="Path to the output JSON file.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Application log level.",
    )
    return parser


def run_pipeline(input_file: str, output_file: str) -> list[ProcessingRecord]:
    """Execute the default processing pipeline."""

    pipeline = DataProcessingPipeline(LOGGER)
    return pipeline.process_file(input_file, output_file, DEFAULT_PIPELINE)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Optional sequence of command-line arguments.

    Returns:
        Process exit code.
    """

    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(getattr(logging, args.log_level))

    input_path = Path(args.input)
    if not input_path.exists():
        LOGGER.error("File not found: %s", input_path)
        return 1

    try:
        results = run_pipeline(args.input, args.output)
    except (DataLoadError, DataProcessingError, DataSaveError):
        return 1

    print(f"Done! Processed {len(results)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
