# Legacy Processor - Refactoring Exercise

This is the starting point for Lab 2: Python Code Refactoring.

## The Challenge

`legacy_processor.py` is working code with many issues:

- No type hints
- Poor variable names (`d`, `t`, `r`, `i`, `f`)
- No error handling (bare `except:`)
- No context managers for file handling
- Magic strings and hardcoded paths
- No documentation
- Deeply nested conditionals
- No tests

## What You'll Do

Use Codex to:
1. Add type hints throughout
2. Rename variables to be descriptive
3. Add proper error handling
4. Use context managers (`with` statements)
5. Extract configuration
6. Add docstrings
7. Write pytest tests
8. Set up code quality tools

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the legacy code
python legacy_processor.py

# After refactoring, run tests
pytest --cov=. --cov-report=html
```

## Usage Examples

Run the calculator Strategy pattern example:

```bash
python examples/calculator_strategy_example.py
```

Run the data-processing Chain of Responsibility example:

```bash
python examples/data_processing_pipeline_example.py
```

The examples show how the refactored modules can be used directly, without the
legacy facade.

## Quality Tools

This lab uses a focused modern toolchain:

```bash
black .
ruff check . --fix
mypy legacy_processor.py src tests examples
pytest
```

Install the pre-commit hooks:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

Or use the Makefile shortcuts:

```bash
make format
make lint
make test
make coverage
make docs
make precommit
```

Build the package locally:

```bash
python -m build
```

## First Codex Prompt

```
Analyze legacy_processor.py and list all the code smells and
issues that need to be fixed. Then start by adding type hints.
```
