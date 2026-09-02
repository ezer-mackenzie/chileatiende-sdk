# Contributing to chileatiende-sdk

First off, thank you for considering contributing to `chileatiende-sdk`!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ezer-mackenzie/chileatiende-sdk.git
   cd chileatiende-sdk
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Run unit tests:
   ```bash
   poetry run pytest
   ```

4. Run code formatting and linting:
   ```bash
   poetry run ruff check .
   poetry run mypy src
   ```

## Pull Request Guidelines

- Ensure all unit tests pass before submitting.
- Maintain 100% type coverage for public classes and methods.
- Update documentation and changelog as appropriate.
