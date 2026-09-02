"""Unit tests for DataFrame export capabilities."""

from chileatiende_sdk.models import Ficha, FichasFeed, Servicio, ServiciosFeed


def test_fichas_feed_to_pandas_import_error() -> None:
    feed = FichasFeed(items=[Ficha(id="1", titulo="Test Ficha")])
    try:
        df = feed.to_pandas()
        assert len(df) == 1
    except ImportError as exc:
        assert "pandas is required" in str(exc)


def test_servicios_feed_to_polars_import_error() -> None:
    feed = ServiciosFeed(items=[Servicio(codigo="AD001", titulo="Test Service")])
    try:
        df = feed.to_polars()
        assert len(df) == 1
    except ImportError as exc:
        assert "polars is required" in str(exc)
