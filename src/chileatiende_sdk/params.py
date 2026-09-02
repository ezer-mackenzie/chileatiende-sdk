"""Parameter encoding and validation utilities for ChileAtiende API endpoints."""

from __future__ import annotations

from typing import Any


class ParameterEncoder:
    """Encoder for query string and URL parameters."""

    @staticmethod
    def compact(params: dict[str, Any]) -> dict[str, Any]:
        """Filter out keys with `None` values."""
        return {k: v for k, v in params.items() if v is not None}

    @staticmethod
    def bool_str(val: bool | None) -> str | None:
        """Convert a boolean to string expected by the API ('true' or 'false')."""
        if val is None:
            return None
        return "true" if val else "false"
