# Legacy Data Processor - Needs Refactoring!
# This code works but has many issues. Use Codex to improve it.

import logging
import os
from typing import Any, Iterable, Mapping, Union

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
RecordInput = Union[Record, Mapping[str, Any]]


def process(d: Iterable[RecordInput], t: ProcessType) -> list[Record]:
    processor = processor_for(t)
    return processor.process(normalize_records(d))


def load_records(filename: str) -> list[Record]:
    with JsonRecordReader(filename) as reader:
        return reader.read()


def load_and_process(f: str, t: ProcessType) -> list[Record]:
    data = load_records(f)
    return process(data, t)


def save_results(data: list[Record], filename: str) -> None:
    with JsonRecordWriter(filename) as writer:
        writer.write(data)


def main() -> None:
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
