install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-pre-commit:
	pre-commit install

style:
	pre-commit run --all-files

test:
	python -m unittest

check: style test