.PHONY: format lint test coverage examples docs precommit clean

PYTHON := .venv/bin/python
PRE_COMMIT := .venv/bin/pre-commit
MYPY_TARGETS := legacy_processor.py src tests examples

format:
	$(PYTHON) -m black .
	$(PYTHON) -m ruff check . --fix

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy $(MYPY_TARGETS)

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov=. --cov-report=term-missing --cov-report=html

examples:
	$(PYTHON) examples/calculator_strategy_example.py
	$(PYTHON) examples/data_processing_pipeline_example.py

docs: examples
	$(PYTHON) -c "import ast; from pathlib import Path; missing = []; paths = [Path('legacy_processor.py'), *Path('src').rglob('*.py'), *Path('examples').rglob('*.py')]; [missing.append(f'{path}:{node.lineno}: {type(node).__name__} {node.name}') for path in paths for node in ast.walk(ast.parse(path.read_text())) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and ast.get_docstring(node) is None]; print('All production/example functions and classes have docstrings') if not missing else (_ for _ in ()).throw(SystemExit('\n'.join(missing)))"

precommit:
	$(PRE_COMMIT) run --all-files

clean:
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache -o -name .ruff_cache -o -name htmlcov \) -prune -exec rm -rf {} +
	rm -f .coverage
