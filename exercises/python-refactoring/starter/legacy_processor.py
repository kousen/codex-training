# Legacy Data Processor - Needs Refactoring!
# This code works but has many issues. Use Codex to improve it.

import logging
import os
from collections.abc import Iterable, Mapping
from typing import Any

from src.data_processing import JsonRecordReader, JsonRecordWriter
from src.data_processing.processors import (
    ProcessType,
    Record,
    build_default_pipeline,
    normalize_records,
    processor_for,
)
from src.exceptions import DataProcessingError

logger = logging.getLogger(__name__)
RecordInput = Record | Mapping[str, Any]


def process(d: Iterable[RecordInput], t: ProcessType) -> list[Record]:
    """Run one legacy processing operation over records.

    Args:
        d: Existing ``Record`` objects or JSON-style record mappings.
        t: Operation to run: ``"filter"``, ``"transform"``, or ``"validate"``.

    Returns:
        Processed records as dataclass instances.

    Raises:
        DataProcessingError: If processing fails.
    """
    processor = processor_for(t)
    return processor.process(normalize_records(d))


def load_records(filename: str) -> list[Record]:
    """Load records from a JSON file.

    Args:
        filename: Path to a JSON file containing record objects.

    Returns:
        Records parsed from the file.

    Raises:
        src.exceptions.DataLoadError: If the file cannot be read or parsed.
    """
    with JsonRecordReader(filename) as reader:
        return reader.read()


def load_and_process(f: str, t: ProcessType) -> list[Record]:
    """Load records from a file and run one processing operation.

    Args:
        f: Path to a JSON input file.
        t: Operation to run after loading records.

    Returns:
        Processed records.

    Raises:
        DataProcessingError: If loading or processing fails.
    """
    data = load_records(f)
    return process(data, t)


def save_results(data: list[Record], filename: str) -> None:
    """Save processed records to a JSON file.

    Args:
        data: Records to write.
        filename: Path to the JSON output file.

    Raises:
        src.exceptions.DataSaveError: If records cannot be written.
    """
    with JsonRecordWriter(filename) as writer:
        writer.write(data)


def main() -> None:
    """Run the default legacy command-line workflow.

    The workflow reads ``/tmp/input.json``, runs the default processing
    pipeline, and writes ``/tmp/output.json``.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    # hardcoded paths
    input_file = "/tmp/input.json"
    output_file = "/tmp/output.json"

    if os.path.exists(input_file):
        try:
            data = load_records(input_file)
            data = build_default_pipeline().process(data)
            save_results(data, output_file)
            logger.info("Done! Processed %s items", len(data))
        except DataProcessingError as error:
            logger.error("Processing failed: %s", error)
    else:
        logger.warning("File not found: %s", input_file)


if __name__ == "__main__":
    main()
