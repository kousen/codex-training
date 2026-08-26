"""Shared JSON record types."""

from typing import TypeAlias

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)
Record: TypeAlias = dict[str, JsonValue]


def clone_json(value: JsonValue) -> JsonValue:
    """Recursively copy a JSON value without sharing mutable containers."""
    if isinstance(value, dict):
        return {key: clone_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clone_json(item) for item in value]
    return value


def clone_record(record: Record) -> Record:
    """Return a deep copy of a JSON record."""
    return {key: clone_json(value) for key, value in record.items()}
