"""Numeric data processing utilities replacing legacy global state."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, List, Tuple

from exceptions.custom import DataProcessingError, ValidationError
from utils.validators import ensure_sequence_min_length, ensure_numeric


@dataclass(slots=True, frozen=True)
class NumericProcessingConfig:
    """Configuration for the numeric processing pipeline."""

    scale: float = 1.5
    offset: float = 10.0
    minimum_output: float = 0.0
    maximum_output: float = 100.0
    minimum_length: int = 5


def _normalise_input(values: Tuple[float, ...]) -> Tuple[float, ...]:
    try:
        return tuple(ensure_numeric(value, name="input item") for value in values)
    except ValidationError as exc:
        raise DataProcessingError("Input data must contain only numeric values") from exc


@lru_cache(maxsize=128)
def _process_tuple(data: Tuple[float, ...], config: NumericProcessingConfig) -> Tuple[float, ...]:  # type: ignore[misc]
    scale, offset = config.scale, config.offset
    minimum, maximum = config.minimum_output, config.maximum_output

    processed = tuple(
        max(minimum, min(value * scale + offset, maximum))
        for value in data
    )
    return processed


def process_numeric_sequence(data: Iterable[float], *, config: NumericProcessingConfig | None = None) -> List[float]:
    """Process numeric data with scaling and clamping rules."""
    active_config = config or NumericProcessingConfig()
    values = tuple(data)
    try:
        ensure_sequence_min_length(values, minimum=active_config.minimum_length, name="input data")
    except ValidationError as exc:
        raise DataProcessingError("Insufficient data provided") from exc
    normalised = _normalise_input(values)
    return list(_process_tuple(normalised, active_config))
