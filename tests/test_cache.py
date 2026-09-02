"""Unit tests for cache storage and client caching layer."""

import time
import respx

from chileatiende_sdk import ClientConfig, InMemoryCacheStorage, SyncChileAtiendeClient


def test_in_memory_cache_storage() -> None:
    cache = InMemoryCacheStorage()
    assert cache.get("key1") is None

    cache.set("key1", "value1", ttl=0.1)
    assert cache.get("key1") == "value1"

    time.sleep(0.15)
    assert cache.get("key1") is None


@respx.mock
def test_client_caching(test_token: str, mock_ficha_data: dict) -> None:
    route = respx.get("https://www.chileatiende.gob.cl/api/fichas/1").respond(
        status_code=200, json=mock_ficha_data
    )

    cache = InMemoryCacheStorage()
    config = ClientConfig(access_token=test_token, cache_storage=cache, cache_ttl=60)
    client = SyncChileAtiendeClient(config=config)

    # First call: hits HTTP
    ficha1 = client.get_ficha(1)
    assert ficha1.id == "1"
    assert route.call_count == 1

    # Second call: served from cache without HTTP request
    ficha2 = client.get_ficha(1)
    assert ficha2.id == "1"
    assert route.call_count == 1
