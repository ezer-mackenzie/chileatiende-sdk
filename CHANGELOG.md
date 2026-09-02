# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-02

### Added
- First stable production release of `chileatiende-sdk`.
- Integrated exponential backoff retries for transient 429/5xx errors in `ClientConfig`.
- Flexible in-memory caching layer via `CacheStorage` & `InMemoryCacheStorage`.
- DataFrame export utilities (`to_pandas()`, `to_polars()`) on `FichasFeed`, `ServiciosFeed`, and `SucursalesFeed`.
- Command Line Interface (CLI) binary `chileatiende` for terminal operations.
- Auto-paginating iterators (`iter_fichas()`, `aiter_fichas()`).
- Clean HTML-stripped text properties on procedure sheets (`Ficha`).

## [0.2.0-alpha.1] - 2026-09-02

### Added
- Auto-paginating iterators: `iter_fichas()` & `iter_fichas_by_servicio()` for `SyncChileAtiendeClient`.
- Async auto-paginating iterators: `aiter_fichas()` & `aiter_fichas_by_servicio()` for `AsyncChileAtiendeClient`.
- HTML stripping helper properties on `Ficha` model (`clean_objetivo`, `clean_beneficiarios`, `clean_costo`, `clean_vigencia`, `clean_plazo`).
- Dependabot configuration for Pip and GitHub Actions (`.github/dependabot.yml`).
- Developer agreements and guidelines in `AGENTS.md` and `CLAUDE.md`.

## [0.1.0] - 2026-09-02

### Added
- Initial release of `chileatiende-sdk`.
- `SyncChileAtiendeClient` and `AsyncChileAtiendeClient` using `httpx`.
- High-level SDK facades (`ChileAtiendeSDK`, `SyncChileAtiendeSDK`, `AsyncChileAtiendeSDK`).
- Strongly typed Pydantic v2 models for `Ficha`, `FichasFeed`, `Servicio`, `ServiciosFeed`, `Sucursal`, and `SucursalesFeed`.
- Custom exception hierarchy (`AuthenticationError`, `NotFoundError`, `RequestValidationError`, `APIError`, `NetworkError`, `RequestTimeoutError`).
- Full unit test suite with `pytest` and `respx`.
- MkDocs documentation setup.
