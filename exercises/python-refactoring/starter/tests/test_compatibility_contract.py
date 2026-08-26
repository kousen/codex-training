"""Executable documentation for intentional changes to the legacy API."""

from datetime import datetime, timezone
from pathlib import Path

import pytest

import legacy_processor
from codex_refactoring.data_processing.models import Record
from codex_refactoring.exceptions import (
    DataReadError,
    RecordValidationError,
    UnknownOperationError,
)


def contract_clock() -> datetime:
    """Return the timestamp used by the documented compatibility contract."""
    return datetime(2026, 8, 26, 15, 30, tzinfo=timezone.utc)


def test_filter_retains_legacy_selection_without_aliasing_records() -> None:
    """Filtering keeps active values but now returns isolated mappings."""
    record: Record = {"id": 1, "name": "Ada", "status": "active"}
    result = legacy_processor.process([record], "filter")
    assert result == [record]
    assert result[0] is not record


def test_transform_replaces_legacy_fixed_date_with_injected_utc_time() -> None:
    """Transformation retains fields but no longer mutates or uses a stale date."""
    record: Record = {"id": 1, "name": "Ada"}
    result = legacy_processor.process([record], "transform", clock=contract_clock)
    assert result[0]["timestamp"] == "2026-08-26T15:30:00Z"
    assert "timestamp" not in record


def test_invalid_record_now_fails_instead_of_being_silently_dropped() -> None:
    """Validation failures are observable rather than converted to empty output."""
    with pytest.raises(RecordValidationError, match="positive integer"):
        legacy_processor.process([{"id": 0, "name": "Ada"}], "validate")


def test_unknown_operation_now_fails_instead_of_returning_empty_output() -> None:
    """Operation typos are explicit application errors."""
    with pytest.raises(UnknownOperationError, match="Unsupported operation"):
        legacy_processor.process([], "typo")


def test_read_error_now_propagates_instead_of_returning_empty_output(
    tmp_path: Path,
) -> None:
    """An absent file is distinguishable from a valid empty JSON array."""
    with pytest.raises(DataReadError, match="Unable to read"):
        legacy_processor.load_and_process(tmp_path / "missing.json", "filter")
