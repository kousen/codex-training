"""Unit tests for data processing pipeline behaviors."""

from __future__ import annotations

import pytest

from data_processing.numeric import NumericProcessingConfig, process_numeric_sequence
from data_processing.service import EmployeeDataService
from exceptions.custom import DataProcessingError


def test_average_salary(employee_service: EmployeeDataService) -> None:
    assert employee_service.average_salary() > 0


def test_find_employee(employee_service: EmployeeDataService) -> None:
    record = employee_service.find("Jane Smith")
    assert record is not None
    assert record.name == "Jane Smith"


def test_filter_by_age(employee_service: EmployeeDataService) -> None:
    filtered = employee_service.filter_by_age(minimum=30, maximum=40)
    assert all(30 <= record.age <= 40 for record in filtered)


def test_sort_by_salary_descending(employee_service: EmployeeDataService) -> None:
    sorted_records = employee_service.sort_by_salary(descending=True)
    salaries = [record.salary for record in sorted_records]
    assert salaries == sorted(salaries, reverse=True)


def test_numeric_processing_sequence_requires_minimum_length() -> None:
    with pytest.raises(DataProcessingError):
        process_numeric_sequence([1, 2, 3, 4])


def test_numeric_processing_applies_scaling_and_clamping() -> None:
    data = [0, 10, 100]
    config = NumericProcessingConfig(minimum_length=3)
    processed = process_numeric_sequence(data, config=config)
    assert processed[0] == 10
    assert processed[-1] == 100


def test_numeric_processing_uses_cache() -> None:
    config = NumericProcessingConfig(minimum_length=5)
    data = [1, 2, 3, 4, 5]
    first = process_numeric_sequence(data, config=config)
    second = process_numeric_sequence(data, config=config)
    assert first == second
    assert first is not second
