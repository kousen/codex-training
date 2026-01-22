"""Entry point for the refactored data processor."""

# ruff: noqa: E402

from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
# Ensure local src packages are importable when running this script directly.
sys.path.insert(0, str(SRC_PATH))
# pylint: disable=wrong-import-position

from data_processing import (  # noqa: E402
    build_default_pipeline,
    read_json_records,
    write_json_records,
)
from exceptions.custom import DataProcessingError  # noqa: E402
from utils.logging import configure_logging  # noqa: E402

INPUT_FILE = Path("/tmp/input.json")
OUTPUT_FILE = Path("/tmp/output.json")

logger = logging.getLogger(__name__)


def run_pipeline(input_path: Path, output_path: Path) -> int:
    """Run the processing pipeline and return the number of records written."""
    records = read_json_records(input_path)
    pipeline = build_default_pipeline()
    processed = pipeline.handle(records)
    write_json_records(output_path, processed)
    return len(processed)


def main() -> None:
    """Run the processor with default configuration."""
    configure_logging()
    if not INPUT_FILE.exists():
        logger.error("Input file not found: %s", INPUT_FILE)
        return

    try:
        count = run_pipeline(INPUT_FILE, OUTPUT_FILE)
    except DataProcessingError as exc:
        logger.exception("Processing failed: %s", exc)
        return

    logger.info("Done! Processed %s items", count)


if __name__ == "__main__":
    main()
