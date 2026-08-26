"""Installable command-line application and compatibility API."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Iterable, Sequence
from os import PathLike

from codex_refactoring.data_processing.models import Record
from codex_refactoring.data_processing.processors import (
    Clock,
    Operation,
    ProcessingPipeline,
    create_processor,
    utc_now,
)
from codex_refactoring.data_processing.readers import read_json_records
from codex_refactoring.data_processing.writers import write_json_records
from codex_refactoring.exceptions import ProcessingError
from codex_refactoring.utils import configure_logging

LOGGER = logging.getLogger(__name__)
PathInput = str | PathLike[str]
DEFAULT_OPERATIONS = tuple(operation.value for operation in Operation)


def process(
    data: Iterable[Record],
    operation: Operation | str,
    *,
    clock: Clock = utc_now,
) -> list[Record]:
    """Process records with one operation.

    This compatibility wrapper retains the legacy function name while using
    the new typed strategy implementation.

    Args:
        data: Records to process.
        operation: Filter, transform, or validate.
        clock: Timestamp source used by transformation.

    Returns:
        Processed record copies.
    """
    return create_processor(operation, clock).process(data)


def load_and_process(
    filename: PathInput,
    operation: Operation | str,
    *,
    clock: Clock = utc_now,
) -> list[Record]:
    """Load JSON records and process them with one operation."""
    return process(read_json_records(filename), operation, clock=clock)


def save_results(data: Iterable[Record], filename: PathInput) -> None:
    """Atomically save records as formatted UTF-8 JSON."""
    write_json_records(data, filename)


def run_pipeline(
    input_file: PathInput,
    output_file: PathInput,
    operations: Sequence[Operation | str] = DEFAULT_OPERATIONS,
    *,
    clock: Clock = utc_now,
) -> list[Record]:
    """Load, process, and save records using configurable operations."""
    pipeline = ProcessingPipeline(
        [create_processor(operation, clock) for operation in operations]
    )
    records = pipeline.process(read_json_records(input_file))
    write_json_records(records, output_file)
    return records


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Filter, transform, and validate records from a JSON file."
    )
    parser.add_argument("input_file", help="path to the input JSON array")
    parser.add_argument("output_file", help="path for processed JSON results")
    parser.add_argument(
        "--operations",
        nargs="+",
        choices=[operation.value for operation in Operation],
        default=list(DEFAULT_OPERATIONS),
        help="operations to run in order (default: filter transform validate)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable debug logging",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line application and return a process exit code."""
    arguments = build_parser().parse_args(argv)
    configure_logging(arguments.verbose)

    try:
        records = run_pipeline(
            arguments.input_file,
            arguments.output_file,
            arguments.operations,
        )
    except ProcessingError as exc:
        LOGGER.error("Processing failed: %s", exc)
        return 1

    LOGGER.info("Processed %d items", len(records))
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised by the interpreter
    raise SystemExit(main())
