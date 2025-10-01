"""Temperature conversion utilities with strong typing."""

from __future__ import annotations

from enum import Enum
from typing import Callable, Dict

from exceptions.custom import TemperatureConversionError
from utils.validators import ensure_numeric


class TemperatureUnit(str, Enum):
    """Supported temperature units."""

    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


_TO_KELVIN: Dict[TemperatureUnit, Callable[[float], float]] = {
    TemperatureUnit.CELSIUS: lambda value: value + 273.15,
    TemperatureUnit.FAHRENHEIT: lambda value: (value - 32) * 5 / 9 + 273.15,
    TemperatureUnit.KELVIN: lambda value: value,
}

_FROM_KELVIN: Dict[TemperatureUnit, Callable[[float], float]] = {
    TemperatureUnit.CELSIUS: lambda value: value - 273.15,
    TemperatureUnit.FAHRENHEIT: lambda value: (value - 273.15) * 9 / 5 + 32,
    TemperatureUnit.KELVIN: lambda value: value,
}


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature between units.

    Args:
        value: Numeric temperature to convert.
        from_unit: Source unit symbol (C, F, K).
        to_unit: Destination unit symbol (C, F, K).

    Returns:
        Converted temperature as a float.

    Raises:
        TemperatureConversionError: If either unit is unsupported.
    """
    canonical_value = ensure_numeric(value, name="temperature")

    try:
        source = TemperatureUnit(from_unit.upper())
        target = TemperatureUnit(to_unit.upper())
    except ValueError as exc:
        raise TemperatureConversionError(f"Unsupported temperature unit: {from_unit} or {to_unit}") from exc

    kelvin = _TO_KELVIN[source](canonical_value)
    converted = _FROM_KELVIN[target](kelvin)

    if target is TemperatureUnit.KELVIN and converted < 0:
        raise TemperatureConversionError("Kelvin temperature cannot be negative")

    return converted


__all__ = ["TemperatureUnit", "convert_temperature"]
