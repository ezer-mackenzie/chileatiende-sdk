"""Asynchronous high-level SDK facade for ChileAtiende."""

from __future__ import annotations

import httpx

from ..clients.async_ import AsyncChileAtiendeClient
from ..config import ClientConfig


class AsyncChileAtiendeSDK:
    """Construct and manage an asynchronous ChileAtiende client."""

    def __init__(
        self,
        access_token: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.client = AsyncChileAtiendeClient(
            access_token=access_token,
            config=config,
            http_client=http_client,
            timeout=timeout,
        )

    async def __aenter__(self) -> AsyncChileAtiendeClient:
        return self.client

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close resources owned by the underlying async HTTP client."""
        await self.client.close()
