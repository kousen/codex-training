"""Pipeline orchestration for the data processor."""

from __future__ import annotations

import logging
from collections.abc import Sequence

from data_processing.models import ProcessingRecord
from data_processing.processors import ProcessingMode, ProcessorFactory
from data_processing.readers import JsonRecordReader
from data_processing.writers import JsonRecordWriter


class DataProcessingPipeline:
    """Chain processors together to handle an end-to-end workflow."""

    def __init__(self, logger: logging.Logger) -> None:
        """Initialize the pipeline with an application logger."""

        self._logger = logger

    def process_records(
        self,
        records: Sequence[ProcessingRecord],
        modes: Sequence[ProcessingMode | str],
    ) -> list[ProcessingRecord]:
        """Run the supplied records through a processor chain."""

        handler_chain = ProcessorFactory.create_chain(modes)
        if handler_chain is None:
            self._logger.debug(
                "No processing modes supplied; returning records unchanged"
            )
            return list(records)

        self._logger.debug(
            "Running handler chain starting with %s against %s records",
            handler_chain.__class__.__name__,
            len(records),
        )
        return handler_chain.handle(records)

    def process_file(
        self,
        input_path: str,
        output_path: str,
        modes: Sequence[ProcessingMode | str],
    ) -> list[ProcessingRecord]:
        """Load, process, and write records using the configured chain."""

        with JsonRecordReader(input_path) as reader:
            records = reader.read()

        processed_records = self.process_records(records, modes)

        with JsonRecordWriter(output_path) as writer:
            writer.write(processed_records)

        self._logger.info(
            "Processed %s records from %s to %s",
            len(processed_records),
            input_path,
            output_path,
        )
        return processed_records
