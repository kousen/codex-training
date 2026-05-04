"""Property-based tests for data-processing behavior."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from data_processing.processors import process_records


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.integers(min_value=-100, max_value=100),
                "name": st.text(max_size=20),
                "status": st.sampled_from(["active", "inactive", "pending"]),
            }
        ),
        max_size=30,
    )
)
def test_filter_only_returns_active_records(records: list[dict[str, object]]) -> None:
    """Filtering never returns inactive records."""

    filtered = process_records(records, "filter")

    assert all(record["status"] == "active" for record in filtered)


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "id": st.integers(min_value=-100, max_value=100),
                "name": st.text(max_size=20),
                "status": st.sampled_from(["active", "inactive", "pending"]),
            }
        ),
        max_size=30,
    )
)
def test_validate_only_returns_positive_ids_and_names(
    records: list[dict[str, object]],
) -> None:
    """Validation only returns positive ids with non-blank names."""

    validated = process_records(records, "validate")

    assert all(
        isinstance(record["id"], int)
        and record["id"] > 0
        and isinstance(record["name"], str)
        and bool(record["name"].strip())
        for record in validated
    )
