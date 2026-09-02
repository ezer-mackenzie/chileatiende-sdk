# Quickstart Guide

## Installation

```bash
pip install chileatiende-sdk
```

## Environment Setup

Export your access token in your terminal environment:

```bash
export CHILEATIENDE_ACCESS_TOKEN="your_access_token_here"
```

## Synchronous Usage

```python
from chileatiende_sdk import ChileAtiendeSDK

with ChileAtiendeSDK() as client:
    ficha = client.get_ficha(1)
    print(f"Title: {ficha.titulo}")
    print(f"Objective: {ficha.clean_objetivo}")

    # Auto-paginating iterator
    for item in client.iter_fichas(query="pension"):
        print(item.titulo)
```

## Asynchronous Usage

```python
import asyncio
from chileatiende_sdk import AsyncChileAtiendeSDK

async def run():
    async with AsyncChileAtiendeSDK() as client:
        servicios = await client.list_servicios()
        print(f"Total Services: {len(servicios.items)}")

asyncio.run(run())
```

## Command Line Interface (CLI)

```bash
chileatiende ficha get 1
chileatiende servicio list
chileatiende sucursal list
```
