.PHONY: dev test lint typecheck build install clean

install:
	pip install -e ".[dev,fastapi]"

test:
	pytest tests/ -v --cov=logsmith --cov-report=term-missing

lint:
	ruff check . --fix

typecheck:
	mypy logsmith/ --ignore-missing-imports

build:
	python -m build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf dist/ build/ .pytest_cache/ coverage.xml
