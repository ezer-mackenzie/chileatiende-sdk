"""Synchronous high-level SDK facade for ChileAtiende."""

from __future__ import annotations

import httpx

from ..clients.sync import SyncChileAtiendeClient
from ..config import ClientConfig


class SyncChileAtiendeSDK:
    """Construct and manage a synchronous ChileAtiende client."""

    def __init__(
        self,
        access_token: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.Client | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.client = SyncChileAtiendeClient(
            access_token=access_token,
            config=config,
            http_client=http_client,
            timeout=timeout,
        )

    def __enter__(self) -> SyncChileAtiendeClient:
        return self.client

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """Close resources owned by the underlying HTTP client."""
        self.client.close()


ChileAtiendeSDK = SyncChileAtiendeSDK
