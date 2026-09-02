"""Configuration management for the ChileAtiende SDK."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Mapping

from .errors import AuthenticationError

DEFAULT_BASE_URL = "https://www.chileatiende.gob.cl/api"
DEFAULT_TIMEOUT = 30.0


@dataclass
class ClientConfig:
    """Configuration settings for ChileAtiende API clients.

    Attributes:
        access_token: API access token. If omitted, resolved from `CHILEATIENDE_ACCESS_TOKEN`.
        base_url: Base URL for ChileAtiende API endpoints.
        timeout: Request timeout in seconds.
        headers: Additional HTTP headers to include with requests.
    """

    access_token: str | None = None
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    headers: Mapping[str, str] | None = None

    def resolved_access_token(self) -> str:
        """Resolve and validate the access token from explicit setting or environment."""
        token = self.access_token or os.environ.get("CHILEATIENDE_ACCESS_TOKEN")
        if not token or not token.strip():
            raise AuthenticationError(
                "ChileAtiende access_token is required. Provide 'access_token' or set "
                "the CHILEATIENDE_ACCESS_TOKEN environment variable."
            )
        return token.strip()
