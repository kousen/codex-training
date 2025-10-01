"""Unit tests for the temperature converter."""

from __future__ import annotations

import math

import pytest

from exceptions.custom import TemperatureConversionError
from temperature.converter import TemperatureUnit, convert_temperature


def test_celsius_to_fahrenheit() -> None:
    assert convert_temperature(0, "C", "F") == pytest.approx(32)


def test_round_trip_conversion() -> None:
    value = 25.3
    fahrenheit = convert_temperature(value, "C", "F")
    celsius = convert_temperature(fahrenheit, "F", "C")
    assert celsius == pytest.approx(value)


def test_invalid_unit_raises() -> None:
    with pytest.raises(TemperatureConversionError):
        convert_temperature(10, "X", "C")


def test_kelvin_cannot_be_negative() -> None:
    with pytest.raises(TemperatureConversionError):
        convert_temperature(-300, "C", TemperatureUnit.KELVIN.value)
