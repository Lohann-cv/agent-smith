install:
	uv venv --python 3.13
	uv sync

run:
	uv run main.py

debug:
	uv run python -m pdb main.py $(MAP)

clean:
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	uv run flake8 . --exclude=.venv
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude "(.venv)"

lint-strict:
	uv run flake8 . --exclude=.venv
	uv run mypy . --strict --exclude "(.venv)"

.PHONY: install run visual debug clean lint lint-strict
