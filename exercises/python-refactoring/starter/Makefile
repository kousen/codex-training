PYTHON ?= python3

.PHONY: format lint typecheck test coverage docs

format:
	$(PYTHON) -m black src tests legacy_processor.py
	$(PYTHON) -m isort src tests legacy_processor.py

lint:
	$(PYTHON) -m ruff check src tests legacy_processor.py
	$(PYTHON) -m flake8 src tests legacy_processor.py
	$(PYTHON) -m pylint src tests legacy_processor.py

typecheck:
	$(PYTHON) -m mypy src

test:
	$(PYTHON) -m pytest -v

coverage:
	$(PYTHON) -m pytest --cov=src --cov=legacy_processor --cov-report=term-missing

docs:
	$(PYTHON) -m sphinx -b html docs docs/_build/html
