# Refactored Data Processor

This project is the completed version of Lab 2: Python Code Refactoring. The
legacy single-file script has been split into a typed package with explicit
models, processors, file I/O classes, tests, quality tooling, and Sphinx docs.

## Features

- Python 3.10+ type hints and strict mypy configuration
- Immutable dataclass model for normalized records
- Strategy and Chain of Responsibility patterns for processing
- Specific custom exceptions with logging
- Context-managed JSON readers and writers
- Pytest, coverage, parameterized tests, and Hypothesis property tests
- Black, isort, ruff, flake8, pylint, pre-commit, and Makefile tasks

## Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python legacy_processor.py --input /tmp/input.json --output /tmp/output.json
```

Example input:

```json
[
  {"id": 1, "name": "Ada", "status": "active"},
  {"id": 2, "name": "Grace", "status": "inactive"},
  {"id": 0, "name": "", "status": "active"}
]
```

The standard pipeline keeps active records, marks them as processed, validates
the result, and writes JSON like this:

```json
[
  {
    "id": 1,
    "name": "Ada",
    "status": "active",
    "processed": true,
    "timestamp": "2024-01-01"
  }
]
```

## Development

```bash
make install
make test
make typecheck
make format
make lint
make docs
```

Or run tools directly:

```bash
source .venv/bin/activate

pytest
mypy
black src tests legacy_processor.py
isort src tests legacy_processor.py
ruff check src tests legacy_processor.py
flake8 src tests legacy_processor.py
pylint src legacy_processor.py
sphinx-build -b html docs docs/_build/html
```

## Architecture

- `data_processing.models`: immutable `DataRecord` domain model
- `data_processing.processors`: operation strategies and processing chain
- `data_processing.readers`: JSON input reader
- `data_processing.writers`: JSON output writer
- `data_processing.pipeline`: high-level orchestration
- `legacy_processor.py`: compatibility CLI and wrapper functions

See `docs/architecture.md` for Mermaid diagrams of the package structure,
runtime flow, processing chain, and class relationships.
