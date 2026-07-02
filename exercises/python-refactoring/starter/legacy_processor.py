# Legacy Data Processor - Needs Refactoring!
# This code works but has many issues. Use Codex to improve it.

import json
import os
from pathlib import Path
from typing import cast

from src.data_processing.processors import (
    ProcessType,
    Record,
    build_default_pipeline,
    processor_for,
)


def process(d: list[Record], t: ProcessType) -> list[Record]:
    processor = processor_for(t)
    return processor.process(d)


def load_and_process(f: str, t: ProcessType) -> list[Record]:
    try:
        with Path(f).open() as file:
            data = cast(list[Record], json.load(file))
        result = process(data, t)
        return result
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_results(data: list[Record], filename: str) -> None:
    Path(filename).write_text(json.dumps(data))


def main() -> None:
    # hardcoded paths
    input_file = "/tmp/input.json"
    output_file = "/tmp/output.json"

    if os.path.exists(input_file):
        with Path(input_file).open() as file:
            data = cast(list[Record], json.load(file))
        data = build_default_pipeline().process(data)
        save_results(data, output_file)
        print("Done! Processed " + str(len(data)) + " items")
    else:
        print("File not found")


if __name__ == "__main__":
    main()
