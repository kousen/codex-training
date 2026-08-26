"""Safe readers for JSON record collections."""

from __future__ import annotations

import json
from os import PathLike
from pathlib import Path

from codex_refactoring.data_processing.models import JsonValue, Record
from codex_refactoring.exceptions import DataReadError, InvalidDataFormatError

PathInput = str | PathLike[str]


def read_json_records(filename: PathInput) -> list[Record]:
    """Read and validate a UTF-8 JSON array of objects.

    Args:
        filename: Path to a JSON document.

    Returns:
        Materialized records from the document.

    Raises:
        DataReadError: If the file cannot be read or decoded.
        InvalidDataFormatError: If the JSON shape is not an array of objects.
    """
    path = Path(filename)
    try:
        with path.open("r", encoding="utf-8") as input_file:
            payload: JsonValue = json.load(input_file)
    except json.JSONDecodeError as exc:
        raise DataReadError(f"Invalid JSON in {path}: {exc.msg}") from exc
    except (OSError, UnicodeError) as exc:
        raise DataReadError(f"Unable to read {path}: {exc}") from exc

    if not isinstance(payload, list):
        raise InvalidDataFormatError(
            f"Expected a JSON array in {path}, got {type(payload).__name__}"
        )

    records: list[Record] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise InvalidDataFormatError(
                f"Expected an object at index {index} in {path}, "
                f"got {type(item).__name__}"
            )
        records.append(item)
    return records
