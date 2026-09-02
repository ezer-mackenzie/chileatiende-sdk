"""Unit tests for AsyncChileAtiendeClient using respx HTTP mocking."""

import pytest
import respx

from chileatiende_sdk.clients import AsyncChileAtiendeClient
from chileatiende_sdk.errors import NotFoundError


@pytest.mark.asyncio
@respx.mock
async def test_async_get_ficha(test_token: str, mock_ficha_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/1").respond(
        status_code=200, json=mock_ficha_data
    )

    async with AsyncChileAtiendeClient(access_token=test_token) as client:
        ficha = await client.get_ficha(1)

    assert ficha.id == "1"
    assert ficha.servicio == "Dirección de Previsión de Carabineros de Chile"


@pytest.mark.asyncio
@respx.mock
async def test_async_list_servicios(test_token: str, mock_servicios_feed_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/servicios").respond(
        status_code=200, json=mock_servicios_feed_data
    )

    async with AsyncChileAtiendeClient(access_token=test_token) as client:
        feed = await client.list_servicios()

    assert len(feed.items) == 1
    assert feed.items[0].codigo == "AD001"


@pytest.mark.asyncio
@respx.mock
async def test_async_404_error(test_token: str) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/servicios/INVALID").respond(status_code=404)

    async with AsyncChileAtiendeClient(access_token=test_token) as client:
        with pytest.raises(NotFoundError):
            await client.get_servicio("INVALID")
