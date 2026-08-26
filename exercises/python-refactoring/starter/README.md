# JSON Data Processor - Refactoring Exercise

This project is the completed refactoring for Lab 2 of the Codex CLI workshop.
It turns the original single-file legacy processor into a typed, tested, and
configurable JSON processing pipeline while retaining the original public
function names as compatibility wrappers.

## Requirements

- Python 3.10 or newer

## Installation

Create and activate a virtual environment, then install the project and its
development tools:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Installing from `requirements.txt` is also supported for workshop use:

```bash
python -m pip install -r requirements.txt
```

## Command-Line Usage

The command requires explicit input and output paths; it no longer depends on
hardcoded `/tmp` files:

```bash
python legacy_processor.py input.json output.json
```

The editable installation also provides the equivalent `legacy-processor`
console command:

```bash
legacy-processor input.json output.json
```

The default pipeline runs `filter`, `transform`, and `validate` in that order.
Choose a different sequence with `--operations`:

```bash
python legacy_processor.py input.json output.json \
  --operations filter validate --verbose
```

Input must be a UTF-8 JSON array of objects. Filtering requires a string
`status` field and retains records whose status is `active`. Transformation
adds `processed: true` and a timezone-aware UTC timestamp without mutating the
input record. Validation fails fast unless `id` is a positive non-boolean
integer and `name` is a nonblank string. Additional fields are preserved.

Expected input or filesystem failures are logged and return exit status 1.
Malformed data is never reported as a successful empty result.

## Compatibility API

The original entry points remain available with type hints and explicit error
behavior:

```python
from legacy_processor import load_and_process, process, save_results

active_records = load_and_process("input.json", "filter")
transformed_records = process(active_records, "transform")
save_results(transformed_records, "output.json")
```

### Intentional Legacy Behavior Changes

| Case | Legacy behavior | Refactored behavior |
|---|---|---|
| Unknown operation | Returned `[]` | Raises `UnknownOperationError` |
| Missing or malformed input | Returned `[]` | Raises a specific read or format error |
| Invalid record | Silently dropped | Fails fast with its index and reason |
| Transformation | Mutated input with `2024-01-01` | Returns a deep copy with an actual UTC timestamp |
| Output failure | Could leak or truncate a file | Raises `DataWriteError` and preserves atomicity |

These changes are asserted in `tests/test_compatibility_contract.py`, making
the compatibility boundary explicit rather than accidental.

## Architecture

```text
legacy_processor.py              # CLI and compatibility wrappers
src/codex_refactoring/
├── data_processing/
│   ├── models.py                # Recursive JSON and record types
│   ├── processors.py            # Strategies and processing pipeline
│   ├── readers.py               # Validated UTF-8 JSON input
│   └── writers.py               # Pre-serialized atomic JSON output
├── exceptions/
│   └── custom.py                # Application exception hierarchy
└── utils/
    └── logging.py               # Logging configuration
tests/                           # Unit, integration, and property tests
```

Each processing operation is a Strategy created by a small factory. A
`ProcessingPipeline` composes those strategies as a Chain of Responsibility.
The clock is injectable for deterministic tests, and all returned records are
recursive copies so nested lists and objects cannot mutate caller-owned input.

## Quality Checks

Run the complete verification suite from this directory:

```bash
black --check legacy_processor.py src tests
ruff check legacy_processor.py src tests
mypy legacy_processor.py src tests
pytest --cov --cov-report=term-missing
```

The suite includes unit, integration, property-based, concurrent-write, real
subprocess CLI, compatibility-contract, and built-wheel installation tests.
The configured coverage threshold is 100%, including branch coverage; that
metric is treated as a structural check rather than proof of complete behavior.

Run the supported-version matrix locally when those interpreters are installed:

```bash
tox
```

The repository workflow runs the same gates on Python 3.10 through 3.14 for
changes to this exercise.

### Pre-commit Checks

Install the hooks once from this directory:

```bash
pre-commit install
```

The hooks enforce repository hygiene, Ruff, Black, and strict mypy before a
commit is created. Run them manually across the exercise with:

```bash
pre-commit run --all-files
```

Tests have a 60-second per-test timeout and a 10-minute session timeout so a
stalled subprocess, build, or concurrent-write test cannot hang CI forever.

### Mutation Testing

Coverage verifies that code executed; mutation testing checks whether the tests
notice behavioral changes. Run it manually rather than on every commit:

```bash
mutmut run
mutmut browse
```

The mutation configuration targets application code and omits the expensive
wheel-packaging smoke test. Mutmut requires a platform with `fork`; Windows
users should run it under WSL.
