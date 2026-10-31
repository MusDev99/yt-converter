.PHONY: install lint typecheck test verify run docker

install:
	uv sync --frozen

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy

test:
	uv run pytest

# Gate for every commit and PR (= CI).
verify: lint typecheck test

run:
	uv run uvicorn ytconv.main:app --reload --host 127.0.0.1 --port 8000

docker:
	docker compose up --build
