# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-02

### Added
- Initial release of `chileatiende-sdk`.
- `SyncChileAtiendeClient` and `AsyncChileAtiendeClient` using `httpx`.
- High-level SDK facades (`ChileAtiendeSDK`, `SyncChileAtiendeSDK`, `AsyncChileAtiendeSDK`).
- Strongly typed Pydantic v2 models for `Ficha`, `FichasFeed`, `Servicio`, `ServiciosFeed`, `Sucursal`, and `SucursalesFeed`.
- Custom exception hierarchy (`AuthenticationError`, `NotFoundError`, `RequestValidationError`, `APIError`, `NetworkError`, `RequestTimeoutError`).
- Full unit test suite with `pytest` and `respx`.
- MkDocs documentation setup.
