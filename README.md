# ChileAtiende Python SDK

[![PyPI version](https://img.shields.io/pypi/v/chileatiende-sdk.svg)](https://pypi.org/project/chileatiende-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/chileatiende-sdk.svg)](https://pypi.org/project/chileatiende-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Codecov](https://codecov.io/gh/ezer-mackenzie/chileatiende-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/ezer-mackenzie/chileatiende-sdk)

A modern, fully typed synchronous and asynchronous Python SDK for consuming the official **ChileAtiende API** provided by the Government of Chile (`https://www.chileatiende.gob.cl/desarrolladores`).

---

## 🚀 Features

- **Full Async & Sync Support**: Built on `httpx` for both synchronous workflows and asynchronous (`async/await`) executions.
- **Auto-Paginating Iterators**: Effortlessly traverse pages with `iter_fichas()` and `aiter_fichas()`.
- **Automatic Retries & Resilience**: Exponential backoff handling transient `429` rate limits and `5xx` server errors.
- **In-Memory Caching Layer**: Pluggable TTL caching layer via `InMemoryCacheStorage`.
- **DataFrame Exports**: Native `.to_pandas()` and `.to_polars()` helper methods on feed objects.
- **CLI Utility**: Command Line Tool `chileatiende` for terminal operations.
- **Plaintext HTML Strippers**: Clean properties (`clean_objetivo`, `clean_beneficiarios`, etc.) for procedure sheets.
- **Pydantic v2 Models**: Strongly typed and validated response models (`Ficha`, `Servicio`, `Sucursal`, feeds, and envelopes).
- **PEP 561 / Strict Mypy**: Fully annotated with type hints, ready for `--strict` mypy type checking.

---

## 📦 Installation

```bash
pip install chileatiende-sdk
```

Or using Poetry:

```bash
poetry add chileatiende-sdk
```

---

## 🔑 Authentication

To make requests to the ChileAtiende API, an `access_token` is required. Set it in your environment:

```bash
export CHILEATIENDE_ACCESS_TOKEN="your_access_token_here"
```

---

## 💡 Quick Examples

### Synchronous Usage & Auto-Pagination

```python
from chileatiende_sdk import ChileAtiendeSDK

with ChileAtiendeSDK(access_token="your_access_token") as client:
    # Fetch a procedure sheet (Ficha) by ID
    ficha = client.get_ficha(1)
    print(f"Title: {ficha.titulo}")
    print(f"Plaintext Objective: {ficha.clean_objetivo}")

    # Auto-iterate through all search results across pages
    for item in client.iter_fichas(query="pension"):
        print(f"- [{item.id}] {item.titulo}")
```

### Asynchronous Usage & Caching

```python
import asyncio
from chileatiende_sdk import AsyncChileAtiendeClient, ClientConfig, InMemoryCacheStorage

async def main():
    cache = InMemoryCacheStorage()
    config = ClientConfig(cache_storage=cache, cache_ttl=3600)

    async with AsyncChileAtiendeClient(config=config) as client:
        # First call fetches from API and caches result
        servicio = await client.get_servicio("AD001")
        print(f"Service: {servicio.titulo}")

        # Subsequent call reads instantly from cache
        cached_servicio = await client.get_servicio("AD001")

asyncio.run(main())
```

### DataFrame Conversion (Pandas & Polars)

```python
with ChileAtiendeSDK() as client:
    feed = client.list_fichas(query="beca")

    # Export to pandas DataFrame
    df_pandas = feed.to_pandas()

    # Export to polars DataFrame
    df_polars = feed.to_polars()
```

---

## 💻 CLI Usage

The package installs a `chileatiende` binary for terminal usage:

```bash
# Get a single procedure sheet
chileatiende ficha get 1

# Search procedure sheets
chileatiende ficha search pension

# List public institutions
chileatiende servicio list

# List branch offices
chileatiende sucursal list
```

---

## 🛠️ API Resource Coverage

| Resource | Method Name | Description |
|---|---|---|
| **Fichas** | `get_ficha(ficha_id)` | Retrieve details for a procedure sheet by ID |
| **Fichas** | `list_fichas(query, max_results, page_token)` | List and search procedure sheets with pagination |
| **Fichas Iterator** | `iter_fichas(query)` / `aiter_fichas(query)` | Auto-paginating iterator across all pages |
| **Fichas by Service** | `list_fichas_by_servicio(servicio_id)` | List procedure sheets for a specific state institution |
| **Servicios** | `get_servicio(servicio_id)` | Retrieve details for a state service/institution |
| **Servicios** | `list_servicios()` | List all state services publishing in ChileAtiende |
| **Sucursales** | `get_sucursal(sucursal_id)` | Retrieve details for a branch office |
| **Sucursales** | `list_sucursales(mobile_offices)` | List branch offices or filter mobile offices |

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for details.
