"""Property-based tests for calculator and data-processing invariants."""

from __future__ import annotations

import math
from typing import Any

from hypothesis import assume, given, settings
from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy

from legacy_processor import process
from src.calculator import (
    AddOperation,
    DivideOperation,
    MultiplyOperation,
    SubtractOperation,
)
from src.data_processing import (
    ActiveRecordFilter,
    Record,
    RequiredFieldsValidator,
)
from src.data_processing.processors import (
    ProcessType,
    build_default_pipeline,
    normalize_records,
)

FILTER_PROCESS: ProcessType = "filter"

numeric_values = st.floats(
    min_value=-1_000_000,
    max_value=1_000_000,
    allow_nan=False,
    allow_infinity=False,
    width=32,
)

record_ids = st.one_of(st.none(), st.integers(min_value=-100, max_value=100))
record_names = st.text(max_size=25)
record_statuses = st.sampled_from(["active", "inactive", "pending", ""])

records = st.builds(
    Record,
    id=record_ids,
    name=record_names,
    status=record_statuses,
    processed=st.booleans(),
    timestamp=st.one_of(st.none(), st.text(max_size=20)),
)

raw_record_mappings: SearchStrategy[dict[str, Any]] = st.fixed_dictionaries(  # type: ignore[misc]
    {
        "id": record_ids,
        "name": record_names,
        "status": record_statuses,
    },
    optional={
        "processed": st.booleans(),
        "timestamp": st.text(max_size=20),
    },
)


@given(numeric_values, numeric_values)
def test_addition_strategy_matches_python_addition(left: float, right: float) -> None:
    assert math.isclose(AddOperation().execute(left, right), left + right)


@given(numeric_values, numeric_values)
def test_subtraction_reverses_addition(left: float, right: float) -> None:
    total = AddOperation().execute(left, right)

    assert math.isclose(
        SubtractOperation().execute(total, right),
        left,
        rel_tol=1e-6,
        abs_tol=1e-6,
    )


@given(numeric_values, numeric_values)
def test_multiplication_is_commutative(left: float, right: float) -> None:
    operation = MultiplyOperation()

    assert math.isclose(operation.execute(left, right), operation.execute(right, left))


@given(numeric_values, numeric_values)
def test_division_reverses_multiplication(left: float, right: float) -> None:
    assume(abs(right) > 1e-6)
    product = MultiplyOperation().execute(left, right)

    assert math.isclose(DivideOperation().execute(product, right), left, rel_tol=1e-6)


@given(st.lists(records, max_size=50))
def test_active_filter_only_returns_active_records(generated: list[Record]) -> None:
    result = ActiveRecordFilter().process(generated)

    assert all(record.status == "active" for record in result)
    assert result == [record for record in generated if record.status == "active"]


@given(st.lists(records, max_size=50))
def test_required_fields_validator_only_returns_valid_records(
    generated: list[Record],
) -> None:
    result = RequiredFieldsValidator().process(generated)

    assert all(
        record.id is not None and record.id > 0 and record.name for record in result
    )
    assert result == [
        record
        for record in generated
        if record.id is not None and record.id > 0 and record.name
    ]


@given(st.lists(raw_record_mappings, max_size=30))
def test_normalize_records_matches_record_factory(
    generated: list[dict[str, Any]],
) -> None:
    assert normalize_records(generated) == [
        Record.from_mapping(raw_record) for raw_record in generated
    ]


@settings(max_examples=75)
@given(st.lists(raw_record_mappings, max_size=40))
def test_default_pipeline_outputs_only_active_valid_processed_records(
    generated: list[dict[str, Any]],
) -> None:
    result = build_default_pipeline().process(normalize_records(generated))

    assert all(record.status == "active" for record in result)
    assert all(record.id is not None and record.id > 0 for record in result)
    assert all(record.name for record in result)
    assert all(record.processed for record in result)
    assert all(record.timestamp == "2024-01-01" for record in result)


@given(st.lists(raw_record_mappings, max_size=30))
def test_legacy_filter_facade_matches_active_filter(
    generated: list[dict[str, Any]],
) -> None:
    assert process(generated, FILTER_PROCESS) == ActiveRecordFilter().process(
        normalize_records(generated)
    )
