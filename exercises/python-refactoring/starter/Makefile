PYTHON := ./.venv/bin/python
PIP := ./.venv/bin/pip
PYTEST := ./.venv/bin/pytest
BLACK := ./.venv/bin/black
ISORT := ./.venv/bin/isort
FLAKE8 := ./.venv/bin/flake8
PYLINT := ./.venv/bin/pylint
MYPY := ./.venv/bin/mypy
SPHINX := ./.venv/bin/sphinx-build

.PHONY: install format lint test docs check

install:
	$(PIP) install -r requirements.txt

format:
	$(BLACK) .
	$(ISORT) .

lint:
	$(BLACK) --check .
	$(ISORT) --check-only .
	$(FLAKE8)
	$(PYLINT) legacy_processor.py src tests
	$(MYPY) legacy_processor.py src tests

test:
	$(PYTEST)

docs:
	$(SPHINX) -b html docs docs/_build/html

check: lint test docs
