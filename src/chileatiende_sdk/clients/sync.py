"""Synchronous client for ChileAtiende API endpoints."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
import time
from typing import Any, Self

import httpx

from ..config import ClientConfig
from ..errors import (
    NetworkError,
    RequestTimeoutError,
    RequestValidationError,
    TransportError,
)
from ..models import (
    Ficha,
    FichasFeed,
    FichasFeedEnvelope,
    SingleFichaResponse,
    SingleServicioResponse,
    SingleSucursalResponse,
    Servicio,
    ServiciosFeed,
    ServiciosFeedEnvelope,
    Sucursal,
    SucursalesFeed,
    SucursalesFeedEnvelope,
)
from ..params import ParameterEncoder
from ..parsers import ResponseParser

NETWORK_EXCEPTIONS = (httpx.ConnectError, httpx.CloseError, httpx.ProtocolError)


class SyncChileAtiendeClient:
    """Synchronous HTTP client for ChileAtiende API."""

    def __init__(
        self,
        access_token: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.Client | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.config = config or ClientConfig(access_token=access_token, timeout=timeout)
        self._token = self.config.resolved_access_token()
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.Client(timeout=self.config.timeout)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._http_client.close()

    def _request(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        query_params = {
            "access_token": self._token,
            "type": "json",
            **(params or {}),
        }
        compact_params = ParameterEncoder.compact(query_params)

        max_attempts = max(1, self.config.max_retries + 1)
        attempts = 0
        last_exc: Exception | None = None

        while attempts < max_attempts:
            attempts += 1
            try:
                response = self._http_client.get(url, params=compact_params, headers=headers)
                if response.status_code in (429, 500, 502, 503, 504) and attempts < max_attempts:
                    time.sleep(self.config.backoff_factor * (2 ** (attempts - 1)))
                    continue
                return ResponseParser.decode_response(response)
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempts < max_attempts:
                    time.sleep(self.config.backoff_factor * (2 ** (attempts - 1)))
                    continue
                raise RequestTimeoutError("ChileAtiende request timed out.") from exc
            except NETWORK_EXCEPTIONS as exc:
                last_exc = exc
                if attempts < max_attempts:
                    time.sleep(self.config.backoff_factor * (2 ** (attempts - 1)))
                    continue
                raise NetworkError("Failed to connect to ChileAtiende API.") from exc

        if last_exc:
            raise TransportError("HTTP transport failure while communicating with ChileAtiende.") from last_exc

    def get_ficha(self, ficha_id: int | str) -> Ficha:
        """Obtain detailed information for a single procedure/sheet (Ficha)."""
        ficha_id_str = str(ficha_id).strip()
        if not ficha_id_str:
            raise RequestValidationError("ficha_id cannot be empty.")

        cache_key = f"ficha:{ficha_id_str}"
        if self.config.cache_storage:
            cached = self.config.cache_storage.get(cache_key)
            if isinstance(cached, Ficha):
                return cached

        payload = self._request(f"fichas/{ficha_id_str}")
        result: Ficha = ResponseParser.parse_model(SingleFichaResponse, payload).ficha if "ficha" in payload else ResponseParser.parse_model(Ficha, payload)

        if self.config.cache_storage:
            self.config.cache_storage.set(cache_key, result, ttl=self.config.cache_ttl)
        return result

    def list_fichas(
        self,
        *,
        query: str | None = None,
        max_results: int = 10,
        page_token: str | None = None,
    ) -> FichasFeed:
        """List procedures/sheets (Fichas) with optional search query and pagination."""
        if not 1 <= max_results <= 100:
            raise RequestValidationError("max_results must be between 1 and 100.")

        params = {
            "query": query,
            "maxResults": max_results,
            "pageToken": page_token,
        }
        payload = self._request("fichas", params=params)
        if "fichas" in payload:
            return ResponseParser.parse_model(FichasFeedEnvelope, payload).fichas
        return ResponseParser.parse_model(FichasFeed, payload)

    def iter_fichas(
        self,
        *,
        query: str | None = None,
        max_results: int = 100,
    ) -> Iterator[Ficha]:
        """Automatically iterate over all Fichas across multiple pages."""
        page_token: str | None = None
        while True:
            feed = self.list_fichas(query=query, max_results=max_results, page_token=page_token)
            yield from feed.items
            if not feed.next_page_token:
                break
            page_token = feed.next_page_token

    def list_fichas_by_servicio(
        self,
        servicio_id: str,
        *,
        max_results: int = 10,
        page_token: str | None = None,
    ) -> FichasFeed:
        """List procedures/sheets (Fichas) offered by a specific public service."""
        servicio_id_clean = servicio_id.strip()
        if not servicio_id_clean:
            raise RequestValidationError("servicio_id cannot be empty.")
        if not 1 <= max_results <= 100:
            raise RequestValidationError("max_results must be between 1 and 100.")

        params = {
            "maxResults": max_results,
            "pageToken": page_token,
        }
        payload = self._request(f"servicios/{servicio_id_clean}/fichas", params=params)
        if "fichas" in payload:
            return ResponseParser.parse_model(FichasFeedEnvelope, payload).fichas
        return ResponseParser.parse_model(FichasFeed, payload)

    def iter_fichas_by_servicio(
        self,
        servicio_id: str,
        *,
        max_results: int = 100,
    ) -> Iterator[Ficha]:
        """Automatically iterate over all Fichas for a specific service across pages."""
        page_token: str | None = None
        while True:
            feed = self.list_fichas_by_servicio(servicio_id, max_results=max_results, page_token=page_token)
            yield from feed.items
            if not feed.next_page_token:
                break
            page_token = feed.next_page_token

    def get_servicio(self, servicio_id: str) -> Servicio:
        """Obtain detailed information for a single public service/institution."""
        servicio_id_clean = servicio_id.strip()
        if not servicio_id_clean:
            raise RequestValidationError("servicio_id cannot be empty.")

        cache_key = f"servicio:{servicio_id_clean}"
        if self.config.cache_storage:
            cached = self.config.cache_storage.get(cache_key)
            if isinstance(cached, Servicio):
                return cached

        payload = self._request(f"servicios/{servicio_id_clean}")
        result: Servicio = ResponseParser.parse_model(SingleServicioResponse, payload).servicio if "servicio" in payload else ResponseParser.parse_model(Servicio, payload)

        if self.config.cache_storage:
            self.config.cache_storage.set(cache_key, result, ttl=self.config.cache_ttl)
        return result

    def list_servicios(self) -> ServiciosFeed:
        """List all public services/institutions registered in ChileAtiende."""
        payload = self._request("servicios")
        if "fichas" in payload or "servicios" in payload:
            return ResponseParser.parse_model(ServiciosFeedEnvelope, payload).feed
        return ResponseParser.parse_model(ServiciosFeed, payload)

    def get_sucursal(self, sucursal_id: str) -> Sucursal:
        """Obtain detailed information for a single branch office (Sucursal)."""
        sucursal_id_clean = sucursal_id.strip()
        if not sucursal_id_clean:
            raise RequestValidationError("sucursal_id cannot be empty.")

        cache_key = f"sucursal:{sucursal_id_clean}"
        if self.config.cache_storage:
            cached = self.config.cache_storage.get(cache_key)
            if isinstance(cached, Sucursal):
                return cached

        payload = self._request(f"sucursales/{sucursal_id_clean}")
        result: Sucursal = ResponseParser.parse_model(SingleSucursalResponse, payload).sucursal if "sucursal" in payload else ResponseParser.parse_model(Sucursal, payload)

        if self.config.cache_storage:
            self.config.cache_storage.set(cache_key, result, ttl=self.config.cache_ttl)
        return result

    def list_sucursales(self, *, mobile_offices: bool | None = None) -> SucursalesFeed:
        """List all branch offices (Sucursales) with optional filter for mobile offices."""
        params = {
            "mobileOffices": ParameterEncoder.bool_str(mobile_offices),
        }
        payload = self._request("sucursales", params=params)
        if "sucursales" in payload:
            return ResponseParser.parse_model(SucursalesFeedEnvelope, payload).sucursales
        return ResponseParser.parse_model(SucursalesFeed, payload)
