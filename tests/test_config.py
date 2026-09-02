"""Unit tests for ClientConfig and token resolution."""

import pytest

from chileatiende_sdk.config import ClientConfig
from chileatiende_sdk.errors import AuthenticationError


def test_config_explicit_token() -> None:
    config = ClientConfig(access_token="my_token")
    assert config.resolved_access_token() == "my_token"


def test_config_env_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHILEATIENDE_ACCESS_TOKEN", "env_token_456")
    config = ClientConfig()
    assert config.resolved_access_token() == "env_token_456"


def test_config_missing_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CHILEATIENDE_ACCESS_TOKEN", raising=False)
    config = ClientConfig()
    with pytest.raises(AuthenticationError, match="access_token is required"):
        config.resolved_access_token()
