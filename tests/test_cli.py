"""Unit tests for ChileAtiende CLI."""

import respx

from chileatiende_sdk.cli import main


def test_cli_help() -> None:
    assert main([]) == 0


@respx.mock
def test_cli_ficha_get(test_token: str, mock_ficha_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/fichas/1").respond(
        status_code=200, json=mock_ficha_data
    )
    assert main(["--token", test_token, "ficha", "get", "1"]) == 0


@respx.mock
def test_cli_servicio_list(test_token: str, mock_servicios_feed_data: dict) -> None:
    respx.get("https://www.chileatiende.gob.cl/api/servicios").respond(
        status_code=200, json=mock_servicios_feed_data
    )
    assert main(["--token", test_token, "servicio", "list"]) == 0
