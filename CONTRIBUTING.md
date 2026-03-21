# Contributing to logsmith

Thank you for your interest in contributing! logsmith is a focused library — small surface area, high quality.

## Development Setup

```bash
git clone https://github.com/Aliipou/logsmith
cd logsmith
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
make test        # run pytest with coverage
make lint        # ruff + mypy
make test-all    # test against Python 3.10, 3.11, 3.12 via tox
```

## Code Style

- ruff for linting and formatting (configured in pyproject.toml)
- mypy for type checking (strict mode)
- All public functions must have type annotations and docstrings

## What We Accept

**High priority:**
- Bug fixes with reproduction cases
- Performance improvements with benchmarks
- New integrations (Sentry, OpenTelemetry, etc.) in `logsmith/integrations/`
- Documentation improvements

**Out of scope:**
- Changing the core JSON schema (breaking change, needs major version)
- Adding runtime dependencies to the core package
- Features that duplicate stdlib logging behavior

## Pull Request Process

1. Open an issue first for non-trivial changes
2. Write tests — coverage must not decrease
3. Update the relevant section of README.md if adding a feature
4. PR title must follow Conventional Commits: `feat:`, `fix:`, `docs:`, `perf:`, `test:`

## Reporting Bugs

Include: Python version, logsmith version, minimal reproduction, expected vs. actual output.
