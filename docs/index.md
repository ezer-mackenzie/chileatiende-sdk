# chileatiende-sdk

Welcome to the official documentation for **chileatiende-sdk**, the modern, fully-typed Python SDK for the ChileAtiende API.

## Core Features

- ⚡ **Sync & Async Support**: First-class async support using `httpx` and `asyncio`.
- 🔄 **Auto-Paginating Iterators**: Effortlessly traverse pages with `iter_fichas()` and `aiter_fichas()`.
- 🛡️ **Pydantic v2 Models**: Robust data validation and field normalization with autocomplete in your IDE.
- 🚀 **Retries & Resilience**: Exponential backoff for 429 rate limits and 5xx errors.
- 💾 **In-Memory Caching**: TTL caching support via `InMemoryCacheStorage`.
- 📊 **DataFrame Exports**: Convert feed results to Pandas or Polars DataFrames.
- 💻 **CLI Utility**: Command line binary `chileatiende` for terminal operations.
- 🔑 **Clean Auth**: Automatic resolution of `access_token` from parameters or `CHILEATIENDE_ACCESS_TOKEN`.
