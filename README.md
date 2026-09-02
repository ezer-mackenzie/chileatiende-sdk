# ChileAtiende Python SDK

[![PyPI version](https://img.shields.io/pypi/v/chileatiende-sdk.svg)](https://pypi.org/project/chileatiende-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/chileatiende-sdk.svg)](https://pypi.org/project/chileatiende-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Codecov](https://codecov.io/gh/ezer-mackenzie/chileatiende-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/ezer-mackenzie/chileatiende-sdk)

A modern, fully typed synchronous and asynchronous Python SDK for consuming the official **ChileAtiende API** provided by the Government of Chile (`https://www.chileatiende.gob.cl/desarrolladores`).

---

## 🚀 Features

- **Full Async & Sync Support**: Built on `httpx` for both synchronous workflows and asynchronous (`async/await`) executions.
- **Pydantic v2 Models**: Strongly typed and validated response models (`Ficha`, `Servicio`, `Sucursal`, feeds, and envelopes).
- **Typed Error Hierarchy**: Clear, actionable exceptions (`AuthenticationError`, `NotFoundError`, `RequestValidationError`, `APIError`).
- **PEP 561 / Strict Mypy**: Fully annotated with type hints, ready for `--strict` mypy type checking.
- **Flexible Authentication**: Configure API credentials via direct parameters or environment variables (`CHILEATIENDE_ACCESS_TOKEN`).

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

To make requests to the ChileAtiende API, an `access_token` is required. You can obtain one from the official developers portal and supply it directly or set it in your environment:

```bash
export CHILEATIENDE_ACCESS_TOKEN="your_access_token_here"
```

---

## 💡 Quick Examples

### Synchronous Usage (`SyncChileAtiendeSDK`)

```python
from chileatiende_sdk import ChileAtiendeSDK

with ChileAtiendeSDK(access_token="your_access_token") as client:
    # Fetch a procedure sheet (Ficha) by ID
    ficha = client.get_ficha(1)
    print(f"Ficha ID: {ficha.id}")
    print(f"Title: {ficha.titulo}")
    print(f"Institution: {ficha.servicio}")

    # Search and list Fichas
    fichas_feed = client.list_fichas(query="pension", max_results=5)
    for item in fichas_feed.items:
        print(f"- {item.titulo}")

    # List all state services/institutions
    servicios_feed = client.list_servicios()
    print(f"Total Institutions: {len(servicios_feed.items)}")
```

### Asynchronous Usage (`AsyncChileAtiendeSDK`)

```python
import asyncio
from chileatiende_sdk import AsyncChileAtiendeSDK

async def main():
    async with AsyncChileAtiendeSDK(access_token="your_access_token") as client:
        # Fetch detailed service information
        servicio = await client.get_servicio("AD001")
        print(f"Service: {servicio.titulo} ({servicio.sigla})")

        # List physical branch offices
        sucursales = await client.list_sucursales(mobile_offices=False)
        print(f"Total Branches: {sucursales.total or len(sucursales.items)}")

asyncio.run(main())
```

---

## 🛠️ API Resource Coverage

| Resource | Method Name | Description |
|---|---|---|
| **Fichas** | `get_ficha(ficha_id)` | Retrieve details for a procedure sheet by ID |
| **Fichas** | `list_fichas(query, max_results, page_token)` | List and search procedure sheets with pagination |
| **Fichas by Service** | `list_fichas_by_servicio(servicio_id)` | List procedure sheets for a specific state institution |
| **Servicios** | `get_servicio(servicio_id)` | Retrieve details for a state service/institution |
| **Servicios** | `list_servicios()` | List all state services publishing in ChileAtiende |
| **Sucursales** | `get_sucursal(sucursal_id)` | Retrieve details for a branch office |
| **Sucursales** | `list_sucursales(mobile_offices)` | List branch offices or filter mobile offices |

---

## 🚨 Exception Handling

```python
from chileatiende_sdk import ChileAtiendeSDK
from chileatiende_sdk.errors import (
    AuthenticationError,
    NotFoundError,
    RequestValidationError,
    APIError,
)

try:
    with ChileAtiendeSDK() as client:
        ficha = client.get_ficha(999999)
except AuthenticationError:
    print("Invalid or missing access token.")
except NotFoundError:
    print("The requested procedure sheet does not exist.")
except RequestValidationError as e:
    print(f"Invalid parameter value: {e}")
except APIError as e:
    print(f"API request error: {e}")
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for details.
