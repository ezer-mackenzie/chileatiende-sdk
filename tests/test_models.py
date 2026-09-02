"""Unit tests for Pydantic models."""

from chileatiende_sdk.models import Ficha, Servicio, Sucursal


def test_ficha_model_parsing(mock_ficha_data: dict) -> None:
    data = mock_ficha_data["ficha"]
    ficha = Ficha.model_validate(data)
    assert ficha.id == "1"
    assert ficha.servicio == "Dirección de Previsión de Carabineros de Chile"
    assert ficha.temas == ["Salud"]
    assert ficha.tags == ["DIPRECA", "Carabineros"]


def test_ficha_model_tag_list_conversion() -> None:
    data = {
        "id": "10",
        "titulo": "Ficha Test",
        "temas": ["Categoria 1", "Categoria 2"],
        "tags": ["TagA", "TagB"],
    }
    ficha = Ficha.model_validate(data)
    assert ficha.temas == ["Categoria 1", "Categoria 2"]
    assert ficha.tags == ["TagA", "TagB"]


def test_ficha_html_stripping() -> None:
    data = {
        "id": "5",
        "titulo": "HTML Test Ficha",
        "objetivo": "<p>Solicitar a la <strong>Dirección</strong> de Previsión.</p>",
        "beneficiarios": "<p>El personal activo y montepiados.</p>",
        "costo": "<p>Ninguno.</p>",
    }
    ficha = Ficha.model_validate(data)
    assert ficha.clean_objetivo == "Solicitar a la Dirección de Previsión."
    assert ficha.clean_beneficiarios == "El personal activo y montepiados."
    assert ficha.clean_costo == "Ninguno."
    assert ficha.clean_vigencia is None


def test_servicio_model_parsing(mock_servicio_data: dict) -> None:
    data = mock_servicio_data["servicio"]
    servicio = Servicio.model_validate(data)
    assert servicio.codigo == "AD001"
    assert servicio.titulo == "Dirección de Previsión de Carabineros de Chile"
    assert servicio.sigla == "DIPRECA"


def test_sucursal_model_parsing(mock_sucursal_data: dict) -> None:
    data = mock_sucursal_data["sucursal"]
    sucursal = Sucursal.model_validate(data)
    assert sucursal.codigo == "SUC001"
    assert sucursal.nombre == "Oficina Central Santiago"
    assert sucursal.comuna == "Santiago"
    assert sucursal.oficina_movil is False
