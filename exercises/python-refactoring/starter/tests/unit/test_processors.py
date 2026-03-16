"""Tests for processor strategies."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from data_processing.models import ProcessingRecord
from data_processing.processors import (
    FilterActiveHandler,
    ProcessingMode,
    ProcessorFactory,
    TransformHandler,
    ValidateHandler,
)
from exceptions.custom import UnsupportedProcessTypeError


@pytest.fixture
def records() -> list[ProcessingRecord]:
    """Create representative domain records."""

    return [
        ProcessingRecord(id=1, name="Alpha", status="active"),
        ProcessingRecord(id=2, name="Beta", status="inactive"),
        ProcessingRecord(id=-1, name="", status="active"),
    ]


@pytest.mark.parametrize(
    ("mode", "expected_class"),
    [
        (ProcessingMode.FILTER, FilterActiveHandler),
        ("transform", TransformHandler),
        ("validate", ValidateHandler),
    ],
)
def test_factory_creates_expected_processor(
    mode: ProcessingMode | str, expected_class: type[object]
) -> None:
    assert isinstance(ProcessorFactory.create(mode), expected_class)


def test_factory_rejects_unknown_mode() -> None:
    with pytest.raises(UnsupportedProcessTypeError):
        ProcessorFactory.create("unknown")


def test_factory_creates_processor_chain() -> None:
    chain = ProcessorFactory.create_chain(
        [ProcessingMode.FILTER, ProcessingMode.TRANSFORM, ProcessingMode.VALIDATE]
    )

    assert chain is not None
    assert chain.__class__.__name__ == "FilterActiveHandler"
    assert chain.next_handler is not None
    assert chain.next_handler.__class__.__name__ == "TransformHandler"
    assert chain.next_handler.next_handler is not None
    assert chain.next_handler.next_handler.__class__.__name__ == "ValidateHandler"


def test_factory_returns_none_for_empty_chain() -> None:
    assert ProcessorFactory.create_chain([]) is None


def test_filter_active_processor(records: list[ProcessingRecord]) -> None:
    filtered = FilterActiveHandler().handle(records)

    assert [record.id for record in filtered] == [1, -1]


def test_transform_processor_is_immutable(records: list[ProcessingRecord]) -> None:
    transformed = TransformHandler(timestamp="2024-06-01").handle(records)

    assert all(record.processed is True for record in transformed)
    assert all(record.timestamp == "2024-06-01" for record in transformed)
    assert all(record.processed is False for record in records)


def test_transform_processor_with_current_date() -> None:
    processor = TransformHandler.with_current_date()

    assert processor.timestamp == datetime.now(tz=timezone.utc).date().isoformat()


def test_validate_processor(records: list[ProcessingRecord]) -> None:
    valid = ValidateHandler().handle(records)

    assert [record.id for record in valid] == [1, 2]


def test_validate_processor_rejects_blank_name() -> None:
    record = ProcessingRecord(id=10, name="   ", status="active")

    assert ValidateHandler().handle([record]) == []


def test_handler_chain_processes_records_in_sequence(
    records: list[ProcessingRecord],
) -> None:
    filter_handler = FilterActiveHandler()
    filter_handler.set_next(TransformHandler(timestamp="2024-06-01")).set_next(
        ValidateHandler()
    )

    processed = filter_handler.handle(records)

    assert [record.id for record in processed] == [1]
    assert processed[0].processed is True
