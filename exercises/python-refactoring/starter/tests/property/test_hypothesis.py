"""Property-based tests for record validation."""

from __future__ import annotations

import pytest

from data_processing.models import Record
from data_processing.processors import ValidateProcessor

hypothesis = pytest.importorskip("hypothesis")
given = hypothesis.given
st = hypothesis.strategies


@given(
    record_id=st.integers(min_value=-5, max_value=5),
    name=st.text(min_size=0, max_size=5),
)
def test_validate_processor_matches_rules(record_id: int, name: str) -> None:
    record = Record(record_id=record_id, name=name)
    result = ValidateProcessor().handle([record])

    should_keep = record_id > 0 and bool(name.strip())
    assert (len(result) == 1) == should_keep
