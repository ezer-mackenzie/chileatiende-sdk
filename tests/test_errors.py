"""Unit tests for exception hierarchy."""

from chileatiende_sdk.errors import (
    APIError,
    AuthenticationError,
    ChileAtiendeError,
    HTTPStatusError,
    NetworkError,
    NotFoundError,
    RequestTimeoutError,
    RequestValidationError,
    TransportError,
)


def test_exception_inheritance() -> None:
    assert issubclass(AuthenticationError, ChileAtiendeError)
    assert issubclass(RequestValidationError, ChileAtiendeError)
    assert issubclass(NotFoundError, ChileAtiendeError)
    assert issubclass(APIError, ChileAtiendeError)
    assert issubclass(HTTPStatusError, APIError)
    assert issubclass(TransportError, ChileAtiendeError)
    assert issubclass(NetworkError, TransportError)
    assert issubclass(RequestTimeoutError, TransportError)


def test_api_error_attributes() -> None:
    err = APIError("Something broke", status_code=500, payload={"detail": "Internal Error"})
    assert str(err) == "Something broke"
    assert err.status_code == 500
    assert err.payload == {"detail": "Internal Error"}
