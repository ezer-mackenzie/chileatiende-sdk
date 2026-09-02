# AGENTS.md

## Project overview

`chileatiende-sdk` is a typed Python 3.12+ client for the ChileAtiende API (`https://www.chileatiende.gob.cl/desarrolladores`). Source code lives in `src/chileatiende_sdk`, tests in `tests`, and MkDocs documentation in `docs`.

API responses are validated directly into Pydantic v2 models under `models`; do not introduce parallel DTO representations.

## Working agreements

- Keep public APIs typed and preserve synchronous (`SyncChileAtiendeClient`) and asynchronous (`AsyncChileAtiendeClient`) behavior.
- Prefer focused changes; do not modify generated `site/` output.
- Never commit credentials or API access tokens.
- Update tests and user-facing documentation when behavior changes.
- Ensure 100% type safety with `mypy --strict`.

## Local validation

Install dependencies with `poetry install`. Before handing off a change, run the checks relevant to it:

```bash
poetry run ruff check .
poetry run mypy src
poetry run pytest -q
poetry run mkdocs build --strict
```

## CI and coverage

The main CI workflow (`.github/workflows/ci.yml`) lints, tests, builds, and validates coverage on Python 3.12 and 3.13.

## Commits

Use concise Conventional Commit-style subjects consistent with the history, such as `feat:`, `fix:`, `test:`, `docs:`, and `ci:`. Include co-author tags when pair programming.
