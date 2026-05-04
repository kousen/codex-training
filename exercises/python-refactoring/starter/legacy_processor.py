"""Compatibility entry point for the refactored data processor.

The original exercise exposed ``process``, ``load_and_process``, and
``save_results`` from this module. They now delegate to the typed package under
``src/data_processing`` while preserving familiar call sites for the lab.
"""

from __future__ import annotations

import argparse
import logging
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from data_processing.models import JsonObject
from data_processing.pipeline import load_process_save
from data_processing.processors import Operation, process_records
from data_processing.readers import JsonFileReader
from data_processing.writers import JsonFileWriter
from exceptions.custom import DataProcessingError
from utils.logging import configure_logging

LOGGER = logging.getLogger(__name__)
DEFAULT_INPUT = Path("/tmp/input.json")
DEFAULT_OUTPUT = Path("/tmp/output.json")


def process(
    data: Sequence[Mapping[str, Any]],
    operation: Operation | str,
) -> list[JsonObject]:
    """Process records with one operation.

    Args:
        data: JSON-like records.
        operation: ``filter``, ``transform``, or ``validate``.

    Returns:
        Processed records as dictionaries.
    """

    return process_records(data, operation)


def load_and_process(
    filename: str | Path,
    operation: Operation | str,
) -> list[JsonObject]:
    """Load JSON records from disk and process them.

    Args:
        filename: Input JSON file.
        operation: Processing operation to apply.

    Returns:
        Processed records, or an empty list when reading/processing fails.
    """

    try:
        data = JsonFileReader().read(filename)
        return process(data, operation)
    except DataProcessingError:
        LOGGER.exception("Could not load and process %s", filename)
        return []


def save_results(data: list[Mapping[str, Any]], filename: str | Path) -> None:
    """Write processed records to disk.

    Args:
        data: JSON-compatible records.
        filename: Output JSON file.
    """

    JsonFileWriter().write(data, filename)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line data processor.

    Args:
        argv: Optional command-line arguments, excluding the executable name.

    Returns:
        Process exit code.
    """

    parser = argparse.ArgumentParser(description="Process a JSON data file.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    configure_logging()

    try:
        count = load_process_save(args.input, args.output)
    except DataProcessingError:
        LOGGER.exception("Data processing failed")
        return 1

    LOGGER.info("Done. Processed %s items", count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
