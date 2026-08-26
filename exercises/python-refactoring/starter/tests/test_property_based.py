"""Property-based tests for invariants across broad record inputs."""

from datetime import datetime, timezone
from pathlib import Path

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from codex_refactoring.data_processing.models import Record
from codex_refactoring.data_processing.processors import (
    ActiveRecordFilter,
    RecordTransformer,
    RecordValidator,
)
from codex_refactoring.data_processing.readers import read_json_records
from codex_refactoring.data_processing.writers import write_json_records

json_scalars = (
    st.none()
    | st.booleans()
    | st.integers()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.text()
)
json_values = st.recursive(
    json_scalars,
    lambda children: st.lists(children, max_size=4)
    | st.dictionaries(st.text(), children, max_size=4),
    max_leaves=12,
)
records = st.lists(st.dictionaries(st.text(), json_values, max_size=6), max_size=8)


@given(
    record_id=st.integers(min_value=1),
    name=st.text(min_size=1).filter(lambda value: bool(value.strip())),
)
def test_all_positive_ids_and_nonblank_names_validate(
    record_id: int, name: str
) -> None:
    """The documented validation domain accepts every generated valid record."""
    record: Record = {"id": record_id, "name": name}
    assert RecordValidator().process([record]) == [record]


@given(
    record_id=st.integers(),
    name=st.text(),
    status=st.sampled_from(["active", "inactive"]),
)
def test_transform_preserves_generated_fields_and_input(
    record_id: int, name: str, status: str
) -> None:
    """Transformation preserves arbitrary input values and never mutates them."""
    record: Record = {"id": record_id, "name": name, "status": status}
    original = dict(record)
    timestamp = datetime(2026, 8, 26, tzinfo=timezone.utc)

    result = RecordTransformer(lambda: timestamp).process([record])[0]

    assert record == original
    assert all(result[key] == value for key, value in original.items())
    assert result["processed"] is True
    assert result["timestamp"] == "2026-08-26T00:00:00Z"


@settings(
    max_examples=75,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
@given(generated_records=records)
def test_arbitrary_json_records_round_trip_through_files(
    tmp_path: Path, generated_records: list[Record]
) -> None:
    """Every supported nested JSON record survives write and read unchanged."""
    destination = tmp_path / "property-roundtrip.json"
    write_json_records(generated_records, destination)
    assert read_json_records(destination) == generated_records


@given(statuses=st.lists(st.sampled_from(["active", "inactive"]), max_size=30))
def test_filter_returns_exactly_active_records_without_aliasing(
    statuses: list[str],
) -> None:
    """Filtering preserves order, selects correctly, and isolates every result."""
    generated: list[Record] = [
        {"id": index + 1, "name": str(index), "status": status}
        for index, status in enumerate(statuses)
    ]

    result = ActiveRecordFilter().process(generated)
    expected = [record for record in generated if record["status"] == "active"]

    assert result == expected
    assert all(
        actual is not original
        for actual, original in zip(result, expected, strict=True)
    )
