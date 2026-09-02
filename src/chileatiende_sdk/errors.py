"""Custom exception hierarchy for the ChileAtiende SDK."""

from __future__ import annotations

from typing import Any


class ChileAtiendeError(Exception):
    """Base exception for all ChileAtiende SDK errors."""


class AuthenticationError(ChileAtiendeError):
    """Raised when authentication credentials (access_token) are missing or invalid."""


class RequestValidationError(ChileAtiendeError):
    """Raised when client-side parameter validation fails."""


class NotFoundError(ChileAtiendeError):
    """Raised when a requested resource (ficha, servicio, sucursal) is not found."""


class APIError(ChileAtiendeError):
    """Raised when the ChileAtiende API returns an error response."""

    def __init__(self, message: str, status_code: int | None = None, payload: Any | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class HTTPStatusError(APIError):
    """Raised for unexpected HTTP status codes."""


class TransportError(ChileAtiendeError):
    """Base class for transport and network layer errors."""


class NetworkError(TransportError):
    """Raised when network connectivity issues occur."""


class RequestTimeoutError(TransportError):
    """Raised when an HTTP request times out."""
