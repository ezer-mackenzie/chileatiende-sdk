"""HTTP Response parsing and deserialization logic for ChileAtiende API."""

from __future__ import annotations

from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from .errors import (
    APIError,
    AuthenticationError,
    HTTPStatusError,
    NotFoundError,
    RequestValidationError,
)

T = TypeVar("T", bound=BaseModel)


class ResponseParser:
    """Decodes HTTP responses and maps JSON data to Pydantic models."""

    @staticmethod
    def decode_response(response: httpx.Response) -> Any:
        """Process response status and decode JSON payload."""
        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed. Please check your ChileAtiende access_token."
            )
        if response.status_code == 404:
            raise NotFoundError(
                f"The requested resource was not found at {response.url.path}."
            )
        if response.status_code >= 400:
            error_text = response.text or f"HTTP {response.status_code}"
            raise HTTPStatusError(
                f"ChileAtiende API error: {error_text}",
                status_code=response.status_code,
            )

        try:
            return response.json()
        except ValueError as exc:
            raise APIError("Failed to decode JSON response from ChileAtiende API.") from exc

    @staticmethod
    def parse_model(model_class: type[T], data: Any) -> T:
        """Parse raw JSON data into a Pydantic model with descriptive error handling."""
        try:
            return model_class.model_validate(data)
        except ValidationError as exc:
            raise RequestValidationError(
                f"Failed to validate {model_class.__name__} data from API response."
            ) from exc
