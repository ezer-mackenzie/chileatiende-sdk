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
    print(ficha.titulo)
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
