"""Safe, atomic writers for JSON record collections."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from collections.abc import Iterable
from os import PathLike
from pathlib import Path

from codex_refactoring.data_processing.models import Record
from codex_refactoring.exceptions import DataWriteError

LOGGER = logging.getLogger(__name__)
PathInput = str | PathLike[str]


def serialize_records(records: Iterable[Record]) -> str:
    """Serialize records before opening a destination file."""
    try:
        return (
            json.dumps(
                list(records),
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )
    except (TypeError, ValueError) as exc:
        raise DataWriteError(f"Unable to serialize results: {exc}") from exc


def write_json_records(records: Iterable[Record], filename: PathInput) -> None:
    """Atomically write records as UTF-8 JSON.

    The payload is serialized first, then written to a temporary sibling and
    atomically moved into place so a failure cannot leave a partial result.
    """
    destination = Path(filename)
    payload = serialize_records(records)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as output_file:
            temporary_path = Path(output_file.name)
            output_file.write(payload)
            output_file.flush()
            os.fsync(output_file.fileno())
        temporary_path.replace(destination)
    except OSError as exc:
        raise DataWriteError(f"Unable to write {destination}: {exc}") from exc
    finally:
        if temporary_path is not None and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                LOGGER.warning("Unable to remove temporary file %s", temporary_path)
