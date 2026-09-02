"""Unit tests for SyncChileAtiendeClient using respx HTTP mocking."""

import pytest
import respx

from chileatiende_sdk.clients import SyncChileAtiendeClient
from chileatiende_sdk.errors import (
    AuthenticationError,
    NotFoundError,
    RequestValidationError,
)


@respx.mock
def test_sync_get_ficha(test_token: str, mock_ficha_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/1").respond(
        status_code=200, json=mock_ficha_data
    )

    client = SyncChileAtiendeClient(access_token=test_token)
    ficha = client.get_ficha(1)

    assert ficha.id == "1"
    assert ficha.servicio == "Dirección de Previsión de Carabineros de Chile"


@respx.mock
def test_sync_list_fichas(test_token: str, mock_fichas_feed_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas").respond(
        status_code=200, json=mock_fichas_feed_data
    )

    client = SyncChileAtiendeClient(access_token=test_token)
    feed = client.list_fichas(max_results=10)

    assert len(feed.items) == 2
    assert feed.next_page_token == "token_next_123"


@respx.mock
def test_sync_get_servicio(test_token: str, mock_servicio_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/servicios/AD001").respond(
        status_code=200, json=mock_servicio_data
    )

    client = SyncChileAtiendeClient(access_token=test_token)
    servicio = client.get_servicio("AD001")

    assert servicio.codigo == "AD001"
    assert servicio.sigla == "DIPRECA"


@respx.mock
def test_sync_list_sucursales(test_token: str, mock_sucursales_feed_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/sucursales").respond(
        status_code=200, json=mock_sucursales_feed_data
    )

    client = SyncChileAtiendeClient(access_token=test_token)
    feed = client.list_sucursales(mobile_offices=False)

    assert feed.total == 1
    assert feed.items[0].codigo == "SUC001"


@respx.mock
def test_sync_401_error(test_token: str) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/99").respond(status_code=401)

    client = SyncChileAtiendeClient(access_token=test_token)
    with pytest.raises(AuthenticationError):
        client.get_ficha(99)


@respx.mock
def test_sync_404_error(test_token: str) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/9999").respond(status_code=404)

    client = SyncChileAtiendeClient(access_token=test_token)
    with pytest.raises(NotFoundError):
        client.get_ficha(9999)


def test_sync_validation_error(test_token: str) -> None:
    client = SyncChileAtiendeClient(access_token=test_token)
    with pytest.raises(RequestValidationError, match="ficha_id cannot be empty"):
        client.get_ficha("   ")

    with pytest.raises(RequestValidationError, match="max_results must be between"):
        client.list_fichas(max_results=0)
