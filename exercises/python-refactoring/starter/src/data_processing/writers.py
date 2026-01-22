"""File writers for data processing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from data_processing.models import Record
from exceptions.custom import DataWriteError


def write_json_records(path: Path, records: Sequence[Record]) -> None:
    """Write records to disk as JSON."""
    payload = [record.to_dict() for record in records]
    try:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)
    except OSError as exc:
        raise DataWriteError(f"Failed to write JSON to {path}") from exc
