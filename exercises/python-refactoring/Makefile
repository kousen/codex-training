.PHONY: format lint type-check test coverage docs all

format:
	poetry run black src tests
	poetry run isort src tests

lint:
	poetry run flake8 src tests
	poetry run pylint src

type-check:
	poetry run mypy src

test:
	poetry run pytest --maxfail=1 --disable-warnings -q

coverage:
	poetry run pytest --cov=src --cov-report=term-missing

docs:
	poetry run sphinx-build -b html docs docs/_build

all: format lint type-check coverage
