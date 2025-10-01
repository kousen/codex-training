# Refactored Python Application

This project modernises the original legacy calculator and data processing script. The refactor embraces clean architecture principles, type safety, and comprehensive testing in line with the project brief.

## Key Capabilities
- Strategy + Factory patterns for calculator operations with validation and logging decorators
- Chain of Responsibility pipeline for employee data, including statistics aggregation and reporting helpers
- Context-managed file readers and writers to eliminate resource leaks
- Configurable numeric data processor that replaces legacy global state with safe caching
- Temperature conversion utilities with exhaustive unit coverage
- Automated logging configuration and reusable validation helpers

## Project Layout
```
src/
├── calculator/
│   ├── calculator.py
│   ├── operations.py
│   └── validators.py
├── data_processing/
│   ├── models.py
│   ├── numeric.py
│   ├── processors.py
│   ├── readers.py
│   ├── service.py
│   └── writers.py
├── exceptions/
│   └── custom.py
├── temperature/
│   └── converter.py
└── utils/
    ├── logging.py
    └── validators.py
```

Tests live under `tests/` and are split into unit, integration, and property-based suites. Documentation sources reside in `docs/` with Sphinx configured for API generation.

## Getting Started
1. Install dependencies (Poetry recommended):
   ```bash
   poetry install --with dev
   ```
2. Run the full quality gate:
   ```bash
   make all
   ```
3. Execute individual checks as needed:
   ```bash
   make format   # Apply black + isort
   make lint     # flake8 + pylint
   make type-check
   make coverage
   ```

Launch the graphical calculator UI:
```bash
PYTHONPATH=src python -m ui.calculator_app
```

## Usage Examples
```python
from calculator.calculator import Calculator

calculator = Calculator()
result = calculator.calculate("mul", 6, 7)
print(result)  # 42.0
```

```python
from ui.calculator_app import launch

launch()
```

```python
from pathlib import Path

from data_processing.service import EmployeeDataService
from data_processing.writers import EmployeeReportWriter

service = EmployeeDataService.from_file("sample_data.csv")
payload = service.generate_report_payload(maximum_age=40)

with EmployeeReportWriter(Path("report.txt")) as writer:
    writer.write(payload)
```

```python
from temperature.converter import convert_temperature

fahrenheit = convert_temperature(21.5, "C", "F")
```

## Quality Tooling
- `black`, `isort` formatting (line length 88)
- `flake8`, `pylint`, `mypy` linting/type checks
- `pytest`, `pytest-cov`, `hypothesis` for testing with 100% coverage target
- Sphinx documentation with Google-style docstrings
- Pre-commit hooks wired for all quality gates

## Documentation
Generate HTML docs with:
```bash
make docs
```
Output is produced under `docs/_build`.

## Contribution Guidelines
- Add type hints and Google-style docstrings to new public APIs
- Prefer pathlib for filesystem access and always use context managers
- Raise specific exceptions, never bare `except`
- Keep cyclomatic complexity under 10 and favour pure functions when practical
- Expand the test suite alongside feature changes to preserve coverage

Enjoy the modernised, maintainable codebase!
