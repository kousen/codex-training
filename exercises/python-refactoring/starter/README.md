# Legacy Processor Refactor

This project refactors a monolithic script into a typed, testable data
processing pipeline with explicit error handling, structured logging,
and automated quality checks.

## Architecture

- `src/calculator/calculator.py`: calculator facade using the Strategy pattern
- `src/calculator/operations.py`: arithmetic strategies and strategy factory
- `legacy_processor.py`: thin compatibility CLI and script entrypoint
- `src/data_processing/models.py`: dataclass-based domain model
- `src/data_processing/processors.py`: Chain of Responsibility handlers and factory
- `src/data_processing/pipeline.py`: file orchestration over the handler chain
- `src/data_processing/readers.py`: JSON reader with context manager support
- `src/data_processing/writers.py`: JSON writer with context manager support
- `src/exceptions/custom.py`: domain-specific exception hierarchy
- `src/utils/logging.py`: logging configuration and decorator support

## Usage

Install dependencies into the existing virtual environment:

```bash
./.venv/bin/pip install -r requirements.txt
```

Run the processor with the default pipeline (`filter -> transform -> validate`):

```bash
./.venv/bin/python legacy_processor.py --input /tmp/input.json --output /tmp/output.json
```

Use the calculator strategies directly:

```python
from calculator.calculator import Calculator

calculator = Calculator()
result = calculator.calculate("multiply", 6, 7)
```

Input files must contain a JSON array of objects. Example:

```json
[
  {"id": 1, "name": "Alpha", "status": "active"},
  {"id": 2, "name": "Beta", "status": "inactive"}
]
```

## Quality Commands

```bash
make format
make lint
make test
make docs
make check
```

## Testing

The suite includes:

- unit tests for models, processors, readers, writers, and logging
- integration tests for the pipeline and CLI compatibility layer
- property-based tests with Hypothesis for validation and transformation rules

Coverage is enforced at 100%.
