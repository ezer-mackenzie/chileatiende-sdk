"""Unit tests for ChileAtiendeSDK facades."""

import pytest
import respx

from chileatiende_sdk.sdk import AsyncChileAtiendeSDK, ChileAtiendeSDK, SyncChileAtiendeSDK


@respx.mock
def test_sync_sdk_context_manager(test_token: str, mock_ficha_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/1").respond(
        status_code=200, json=mock_ficha_data
    )

    with ChileAtiendeSDK(access_token=test_token) as client:
        ficha = client.get_ficha(1)
        assert ficha.id == "1"

    with SyncChileAtiendeSDK(access_token=test_token) as client:
        ficha = client.get_ficha(1)
        assert ficha.id == "1"


@pytest.mark.asyncio
@respx.mock
async def test_async_sdk_context_manager(test_token: str, mock_ficha_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/1").respond(
        status_code=200, json=mock_ficha_data
    )

    async with AsyncChileAtiendeSDK(access_token=test_token) as client:
        ficha = await client.get_ficha(1)
        assert ficha.id == "1"
