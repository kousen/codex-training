"""Output writers for data-processing workflows."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from exceptions.custom import WriterError


class JsonFileWriter:
    """Write records to a JSON file using a context manager."""

    def write(self, records: Sequence[Mapping[str, Any]], path: Path | str) -> None:
        """Write JSON records to ``path``.

        Args:
            records: JSON-compatible mappings.
            path: Output file path.

        Raises:
            WriterError: If the destination cannot be written.
        """

        file_path = Path(path)
        try:
            with file_path.open("w", encoding="utf-8") as output_file:
                json.dump(records, output_file, indent=2)
                output_file.write("\n")
        except (TypeError, OSError) as exc:
            raise WriterError(f"Could not write output file: {file_path}") from exc
