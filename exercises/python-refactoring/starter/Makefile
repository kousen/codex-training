PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: venv install test coverage typecheck format lint docs clean

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -r requirements.txt

test:
	$(BIN)/pytest

coverage:
	$(BIN)/pytest --cov=src --cov=legacy_processor --cov-report=html

typecheck:
	$(BIN)/mypy

format:
	$(BIN)/black src tests legacy_processor.py
	$(BIN)/isort src tests legacy_processor.py

lint:
	$(BIN)/ruff check src tests legacy_processor.py
	$(BIN)/flake8 src tests legacy_processor.py
	$(BIN)/pylint src legacy_processor.py

docs:
	$(BIN)/sphinx-build -b html docs docs/_build/html

clean:
	rm -rf .coverage htmlcov docs/_build .mypy_cache .pytest_cache .ruff_cache
