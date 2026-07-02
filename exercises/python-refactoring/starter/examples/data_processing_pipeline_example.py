"""Usage example for the data-processing Chain of Responsibility."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    """Run a complete JSON read-process-write example."""
    from src.data_processing import JsonRecordReader, JsonRecordWriter
    from src.data_processing.processors import build_default_pipeline

    raw_records = [
        {"id": 1, "name": "Ada", "status": "active"},
        {"id": 2, "name": "Grace", "status": "inactive"},
        {"id": 0, "name": "Barbara", "status": "active"},
    ]

    with TemporaryDirectory() as workspace:
        input_file = Path(workspace) / "input.json"
        output_file = Path(workspace) / "output.json"
        input_file.write_text(json.dumps(raw_records))

        with JsonRecordReader(str(input_file)) as reader:
            records = reader.read()

        processed_records = build_default_pipeline().process(records)

        with JsonRecordWriter(str(output_file)) as writer:
            writer.write(processed_records)

        print(output_file.read_text())


if __name__ == "__main__":
    main()
