"""Property-based tests for processing rules."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from calculator.calculator import Calculator
from data_processing.models import ProcessingRecord
from data_processing.processors import TransformHandler, ValidateHandler


@given(
    st.lists(
        st.builds(
            ProcessingRecord,
            id=st.one_of(st.none(), st.integers()),
            name=st.one_of(st.none(), st.text()),
            status=st.one_of(st.none(), st.sampled_from(["active", "inactive"])),
            processed=st.booleans(),
            timestamp=st.one_of(st.none(), st.text()),
            extra_fields=st.dictionaries(st.text(min_size=1), st.integers()),
        )
    )
)
def test_transform_sets_processed_and_preserves_count(
    records: list[ProcessingRecord],
) -> None:
    transformed = TransformHandler(timestamp="2024-07-04").handle(records)

    assert len(transformed) == len(records)
    assert all(record.processed is True for record in transformed)
    assert all(record.timestamp == "2024-07-04" for record in transformed)


@given(
    st.integers(),
    st.one_of(st.none(), st.text()),
)
def test_validate_enforces_positive_id_and_non_blank_name(
    identifier: int, name: str | None
) -> None:
    record = ProcessingRecord(id=identifier, name=name, status="active")
    validated = ValidateHandler().handle([record])

    expected_is_valid = bool(identifier > 0 and name is not None and name.strip())
    assert (validated == [record]) is expected_is_valid


@given(
    st.floats(allow_nan=False, allow_infinity=False),
    st.floats(allow_nan=False, allow_infinity=False),
)
def test_calculator_addition_is_commutative(left: float, right: float) -> None:
    calculator = Calculator()

    assert calculator.calculate("add", left, right) == calculator.calculate(
        "add", right, left
    )
