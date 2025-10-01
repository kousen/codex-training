"""Property-based tests validating numeric stability."""

from __future__ import annotations

import pytest

pytest.importorskip("hypothesis")

from hypothesis import given, strategies as st
from hypothesis.strategies import SearchStrategy

from temperature.converter import TemperatureUnit, convert_temperature


def _value_strategy(unit: TemperatureUnit) -> SearchStrategy[float]:
    if unit is TemperatureUnit.CELSIUS:
        return st.floats(min_value=-273.15, max_value=1e6, allow_nan=False, allow_infinity=False)
    if unit is TemperatureUnit.KELVIN:
        return st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False)
    return st.floats(min_value=-459.67, max_value=1e6, allow_nan=False, allow_infinity=False)


@st.composite
def temperature_samples(draw) -> tuple[float, TemperatureUnit]:
    unit = draw(st.sampled_from(list(TemperatureUnit)))
    value = draw(_value_strategy(unit))
    return value, unit


@given(temperature_samples(), st.sampled_from(list(TemperatureUnit)))
def test_temperature_round_trip(sample: tuple[float, TemperatureUnit], destination: TemperatureUnit) -> None:
    value, source = sample
    converted = convert_temperature(value, source.value, destination.value)
    round_trip = convert_temperature(converted, destination.value, source.value)
    assert round_trip == pytest.approx(value, rel=1e-6, abs=1e-6)
