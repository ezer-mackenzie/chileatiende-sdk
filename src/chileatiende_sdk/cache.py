"""Caching layer for ChileAtiende SDK."""

from __future__ import annotations

from abc import ABC, abstractmethod
import time
from typing import Any


class CacheStorage(ABC):
    """Abstract protocol for cache storage implementations."""

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Retrieve a cached value if present and unexpired."""

    @abstractmethod
    def set(self, key: str, value: Any, ttl: float = 3600.0) -> None:
        """Store a value in cache with an expiration TTL in seconds."""

    @abstractmethod
    def clear(self) -> None:
        """Clear all entries from cache."""


class InMemoryCacheStorage(CacheStorage):
    """In-memory cache with TTL expiration support."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        if key not in self._store:
            return None
        value, expires_at = self._store[key]
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: float = 3600.0) -> None:
        expires_at = time.time() + ttl
        self._store[key] = (value, expires_at)

    def clear(self) -> None:
        self._store.clear()
