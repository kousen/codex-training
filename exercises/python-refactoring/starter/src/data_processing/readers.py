"""File readers for data processing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from data_processing.models import Record
from exceptions.custom import DataLoadError, DataValidationError


def read_json_records(path: Path) -> list[Record]:
    """Read JSON records from disk."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw_data: Any = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise DataLoadError(f"Failed to read JSON from {path}") from exc

    if not isinstance(raw_data, list):
        raise DataValidationError("Input JSON must be a list of records")

    records: list[Record] = []
    for item in raw_data:
        if not isinstance(item, dict):
            raise DataValidationError("Each record must be a JSON object")
        records.append(Record.from_mapping(item))

    return records
