"""Unit tests for data models."""

from __future__ import annotations

import pytest

from data_processing.models import Record
from exceptions.custom import DataValidationError


def test_record_from_mapping_success() -> None:
    record = Record.from_mapping({"id": 1, "name": "Ada", "status": "active"})

    assert record.record_id == 1
    assert record.name == "Ada"
    assert record.status == "active"
    assert record.processed is False
    assert record.timestamp is None


def test_record_from_mapping_rejects_missing_fields() -> None:
    with pytest.raises(DataValidationError):
        Record.from_mapping({"id": 1})


def test_record_from_mapping_coerces_values() -> None:
    record = Record.from_mapping({"id": "7", "name": 42})
    assert record.record_id == 7
    assert record.name == "42"


def test_record_to_dict_excludes_optional_missing() -> None:
    record = Record(record_id=1, name="Ada")
    assert record.to_dict() == {"id": 1, "name": "Ada", "processed": False}
