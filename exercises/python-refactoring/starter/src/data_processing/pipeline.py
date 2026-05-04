"""High-level orchestration for reading, processing, and writing records."""

from __future__ import annotations

import logging
from pathlib import Path

from data_processing.models import DataRecord
from data_processing.processors import DEFAULT_TIMESTAMP, ProcessingChain
from data_processing.readers import JsonFileReader
from data_processing.writers import JsonFileWriter
from utils.logging import log_call

LOGGER = logging.getLogger(__name__)


class DataProcessingPipeline:
    """Coordinate file I/O with the processing chain."""

    def __init__(
        self,
        reader: JsonFileReader | None = None,
        writer: JsonFileWriter | None = None,
        chain: ProcessingChain | None = None,
    ) -> None:
        """Create a pipeline with injectable collaborators."""

        self.reader = reader or JsonFileReader()
        self.writer = writer or JsonFileWriter()
        self.chain = chain or ProcessingChain.standard()

    @log_call(LOGGER)
    def process_file(self, input_path: Path | str, output_path: Path | str) -> int:
        """Read, process, and write a JSON file.

        Args:
            input_path: Source JSON file.
            output_path: Destination JSON file.

        Returns:
            Number of records written.
        """

        raw_records = self.reader.read(input_path)
        processed_records = self.chain.run(_normalize_records(raw_records))
        output_records = [record.to_dict() for record in processed_records]
        self.writer.write(output_records, output_path)
        return len(output_records)


def load_process_save(
    input_path: Path | str,
    output_path: Path | str,
    *,
    timestamp: str = DEFAULT_TIMESTAMP,
) -> int:
    """Run the standard data-processing pipeline.

    Args:
        input_path: Source JSON file.
        output_path: Destination JSON file.
        timestamp: Processing timestamp for transformed records.

    Returns:
        Number of records written.
    """

    pipeline = DataProcessingPipeline(chain=ProcessingChain.standard(timestamp))
    return pipeline.process_file(input_path, output_path)


def _normalize_records(raw_records: list[dict[str, object]]) -> list[DataRecord]:
    """Convert raw dictionaries to domain records.

    This helper keeps the public pipeline method focused on orchestration.
    """

    return [DataRecord.from_mapping(record) for record in raw_records]
