POETRY_VERSION = 1.2.1

# Env stuff
.PHONY: get-poetry
get-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --version $(POETRY_VERSION)

.PHONY: build-env
build-env:
	python3.10 -m venv .venv
	poetry run pip install --upgrade pip
	poetry run poetry install

# Tests
.PHONY: tests
tests:
	poetry run pytest

# Passive linters
.PHONY: black
black:
	poetry run black split tests --check

.PHONY: flake8
flake8:
	poetry run flake8 split tests

.PHONY: isort
isort:
	poetry run isort split tests --profile=black --check

.PHONY: pylint
pylint:
	poetry run pylint split tests

.PHONY: mypy
mypy:
	poetry run mypy split

# Aggresive linters
.PHONY: black!
black!:
	poetry run black split tests

.PHONY: isort!
isort!:
	poetry run isort split tests --profile=black
