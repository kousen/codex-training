"""Shared pytest fixtures for the refactored project."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from data_processing.service import EmployeeDataService
from utils.logging import configure_logging


@pytest.fixture(scope="session", autouse=True)
def _configure_logging() -> None:
    configure_logging()


@pytest.fixture(scope="session")
def sample_data_path() -> Path:
    root = Path(__file__).resolve().parent.parent
    return root / "sample_data.csv"


@pytest.fixture()
def employee_service(sample_data_path: Path) -> Iterator[EmployeeDataService]:
    service = EmployeeDataService.from_file(sample_data_path)
    yield service
