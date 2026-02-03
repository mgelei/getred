# Repository Guidelines

## Project Structure & Module Organization
- `src/getred/`: Python package (CLI + fetch/parse/save pipeline)
  - `cli.py` (Click entrypoint), `fetcher.py` (httpx client), `parser.py`, `models.py`, `utils.py`
- `tests/`: pytest suite and fixtures (`tests/conftest.py`)
- `pyproject.toml`: packaging (hatchling), dependencies, and pytest config
- `.github/workflows/`: CI (PR tests, version bump check, publish)

## Build, Test, and Development Commands
- Create a venv: `python -m venv .venv && source .venv/bin/activate`
- Install (editable + tests): `python -m pip install -U pip && python -m pip install -e ".[test]"`
- Run locally: `getred "<thread_url>"` or `python -m getred "<thread_url>"`
- Run tests: `pytest`
- Build artifacts (sdist/wheel): `python -m pip install build && python -m build`

## Coding Style & Naming Conventions
- Python 3.12+ (CI uses 3.12); keep code compatible with the declared minimum.
- 4-space indentation, PEP 8, and small focused functions.
- Naming: `snake_case` (functions/vars), `PascalCase` (classes), `UPPER_SNAKE_CASE` (constants).
- Prefer `pathlib.Path` for file paths and keep dependencies minimal (edit `pyproject.toml`).

## Testing Guidelines
- Use pytest; keep tests in `tests/` and name files `test_*.py`.
- Prefer deterministic tests: avoid live Reddit calls (mock httpx or use fixtures).
- Add/adjust tests alongside behavior changes (parser edge-cases, URL validation, output shape).

## Commit & Pull Request Guidelines
- Commit messages follow a Conventional Commits-style prefix used in this repo: `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`, `cicd: ...`.
- PRs should include: what changed, why, how to test (`pytest`), and any user-facing CLI/output changes.
- Versioning: PRs to `master` must bump `version = "..."` in `pyproject.toml` (CI enforces this); keep other version strings (e.g. `src/getred/__init__.py#__version__`) consistent when releasing.
