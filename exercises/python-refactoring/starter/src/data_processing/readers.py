"""Input readers for data-processing workflows."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from exceptions.custom import InvalidDataError, ReaderError


class JsonFileReader:
    """Read records from a JSON file using a context manager."""

    def read(self, path: Path | str) -> list[dict[str, Any]]:
        """Read a JSON array of objects from ``path``.

        Args:
            path: JSON file path.

        Returns:
            A list of JSON objects.

        Raises:
            ReaderError: If the file cannot be read or JSON is malformed.
            InvalidDataError: If the JSON root is not a list of objects.
        """

        file_path = Path(path)
        try:
            with file_path.open("r", encoding="utf-8") as input_file:
                data = json.load(input_file)
        except FileNotFoundError as exc:
            raise ReaderError(f"Input file not found: {file_path}") from exc
        except PermissionError as exc:
            raise ReaderError(f"Input file is not readable: {file_path}") from exc
        except json.JSONDecodeError as exc:
            raise ReaderError(f"Input file contains invalid JSON: {file_path}") from exc
        except OSError as exc:
            raise ReaderError(f"Could not read input file: {file_path}") from exc

        if not isinstance(data, list):
            raise InvalidDataError("Input JSON must be a list of objects")
        if not all(isinstance(item, dict) for item in data):
            raise InvalidDataError("Every input item must be a JSON object")
        return data
