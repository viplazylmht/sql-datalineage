install-pre-commit:
	uv run -- pre-commit install

style:
	uv run -- pre-commit run --all-files

test:
	uv run --no-project -- python -m unittest

check: style test
