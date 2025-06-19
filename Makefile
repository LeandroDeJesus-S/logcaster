.PHONY: check lint format test

check: lint format test

lint:
	poetry run mypy ./logcaster
	poetry run ruff check ./logcaster

format:
	poetry run ruff format ./logcaster

test:
	poetry run pytest ./tests
