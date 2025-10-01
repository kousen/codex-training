"""Unit tests for validator utilities."""

from __future__ import annotations

import pytest

from exceptions.custom import ValidationError
from utils.validators import ensure_non_empty_string, ensure_numeric, ensure_sequence_min_length


def test_ensure_numeric_accepts_int() -> None:
    assert ensure_numeric(10) == 10.0


def test_ensure_numeric_rejects_nan() -> None:
    with pytest.raises(ValidationError):
        ensure_numeric(float("nan"))


def test_ensure_non_empty_string_trims() -> None:
    assert ensure_non_empty_string("  hello  ") == "hello"


def test_sequence_min_length_requires_threshold() -> None:
    with pytest.raises(ValidationError):
        ensure_sequence_min_length([], minimum=1)
